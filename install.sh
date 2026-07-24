#!/bin/bash
# NSSP Lilith OS - Installer for nvme0n1 (500GB)
# Run from live ISO as root

set -euo pipefail

DISK="${1:-/dev/nvme0n1}"
PASSPHRASE="1385"
HOSTNAME="lilith"
USERNAME="tehlappy"

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

if [[ ! -b "$DISK" ]]; then
   echo "Disk $DISK not found"
   lsblk
   exit 1
fi

echo "=== NSSP Lilith OS Installer ==="
echo "Target disk: $DISK"
echo "This will DESTROY all data on $DISK"
read -p "Continue? (yes/no): " CONFIRM
[[ "$CONFIRM" != "yes" ]] && exit 1

# 1. Wipe and partition
echo "=== Partitioning $DISK ==="
sgdisk -Z "$DISK"
sgdisk -n 1:0:+1G   -t 1:ef00 -c 1:"EFI"      "$DISK"
sgdisk -n 2:0:+32G  -t 2:8200 -c 2:"SWAP"     "$DISK"
sgdisk -n 3:0:0     -t 3:8300 -c 3:"ROOT"     "$DISK"
partprobe "$DISK"
sleep 2

# 2. LUKS2 on root partition
echo "=== Creating LUKS2 encryption on ${DISK}p3 ==="
echo -n "$PASSPHRASE" | cryptsetup luksFormat --type luks2 \
  --cipher aes-xts-plain64 --hash sha256 --key-size 512 \
  --pbkdf argon2id --iter-time 4000 --pbkdf-memory 1048576 --pbkdf-parallel 4 \
  "${DISK}p3" -
echo -n "$PASSPHRASE" | cryptsetup open "${DISK}p3" cryptroot -

# 3. Btrfs with subvolumes
echo "=== Creating Btrfs filesystem with subvolumes ==="
mkfs.btrfs -L LILITH_ROOT /dev/mapper/cryptroot
mount /dev/mapper/cryptroot /mnt

for sv in @ @home @snapshots @var_log @var_cache @opt @srv @lilith; do
  btrfs su cr /mnt/$sv
done
umount /mnt

# 4. Mount subvolumes
echo "=== Mounting subvolumes ==="
MOUNT_OPTS="subvol=@,compress=zstd:3,noatime,ssd,discard=async,space_cache=v2"
mount -o "$MOUNT_OPTS" /dev/mapper/cryptroot /mnt

mkdir -p /mnt/{boot/efi,home,.snapshots,var/log,var/cache,opt,srv}
mkdir -p "/mnt/home/$USERNAME/🜏 Lilith/ONE FUCKING DASHBOARD"

mount -o "subvol=@home,$MOUNT_OPTS" /dev/mapper/cryptroot /mnt/home
mount -o "subvol=@snapshots,$MOUNT_OPTS" /dev/mapper/cryptroot /mnt/.snapshots
mount -o "subvol=@var_log,$MOUNT_OPTS" /dev/mapper/cryptroot /mnt/var/log
mount -o "subvol=@var_cache,$MOUNT_OPTS" /dev/mapper/cryptroot /mnt/var/cache
mount -o "subvol=@opt,$MOUNT_OPTS" /dev/mapper/cryptroot /mnt/opt
mount -o "subvol=@srv,$MOUNT_OPTS" /dev/mapper/cryptroot /mnt/srv
mount -o "subvol=@lilith,$MOUNT_OPTS" /dev/mapper/cryptroot "/mnt/home/$USERNAME/🜏 Lilith/ONE FUCKING DASHBOARD"

mkfs.vfat -F32 -n LILITH_EFI "${DISK}p1"
mount "${DISK}p1" /mnt/boot/efi

mkswap -L LILITH_SWAP "${DISK}p2"
swapon "${DISK}p2"

# 5. Install base system
echo "=== Installing base system ==="
pacstrap -K /mnt base linux-zen linux-zen-headers linux-firmware \
  btrfs-progs cryptsetup lvm2 \
  systemd systemd-ukify mkinitcpio \
  networkmanager \
  sudo fish git age sops chezmoi snapper \
  sbctl \
  nvidia nvidia-utils nvidia-settings \
  intel-ucode amd-ucode

# 6. Generate fstab
genfstab -U /mnt >> /mnt/etc/fstab

# 7. Crypttab for initramfs
ROOT_UUID=$(blkid -s UUID -o value "${DISK}p3")
echo "cryptroot UUID=$ROOT_UUID none luks,discard" > /mnt/etc/crypttab.initramfs

# 8. Configure mkinitcpio
arch-chroot /mnt cat > /etc/mkinitcpio.conf.d/nssp.conf << 'EOF'
MODULES=(btrfs nvidia nvidia_modeset nvidia_uvm nvidia_drm)
BINARIES=(/usr/bin/btrfs /usr/sbin/cryptsetup)
FILES=()
HOOKS=(base systemd autodetect microcode modconf kms keyboard keymap consolefont block encrypt btrfs filesystems fsck)
COMPRESSION="zstd"
COMPRESSION_OPTIONS=(-3)
EOF

# 9. Configure kernel command line for UKI
arch-chroot /mnt cat > /etc/kernel/cmdline << EOF
root=LABEL=LILITH_ROOT rootflags=subvol=@,compress=zstd:3,noatime rw quiet loglevel=3 systemd.show_status=auto rd.udev.log_level=3 nvidia_drm.modeset=1
EOF

# 10. Install systemd-boot + UKI
arch-chroot /mnt bootctl install
arch-chroot /mnt kernel-install add "$(pacman -Q linux-zen | cut -d' ' -f2)" /boot

# 11. Copy overlays and run post-install
echo "=== Applying overlays and post-install ==="
rsync -a /home/tehlappy/nssp-build/overlays/ /mnt/ 2>/dev/null || true
arch-chroot /mnt /home/tehlappy/nssp-build/scripts/post-install.sh

# 12. Create user and setup
arch-chroot /mnt useradd -m -G wheel,kvm,render,video,docker,libvirt,input -s /usr/bin/fish "$USERNAME"
arch-chroot /mnt echo "$USERNAME:$PASSPHRASE" | chpasswd
arch-chroot /mnt echo "root:$PASSPHRASE" | chpasswd

# 13. Sign UKI for Secure Boot
arch-chroot /mnt sbctl sign -s /boot/EFI/Linux/lilith-os.efi

# 14. Configure snapper
arch-chroot /mnt snapper -c root create-config /
arch-chroot /mnt snapper -c home create-config /home

# 15. Enable services
arch-chroot /mnt systemctl enable NetworkManager systemd-timesyncd fstrim.timer paccache.timer
arch-chroot /mnt systemctl enable snapper-timeline.timer snapper-cleanup.timer btrfs-scrub@-.timer
arch-chroot /mnt systemctl enable nvidia-suspend nvidia-hibernate nvidia-resume
arch-chroot /mnt systemctl enable ollama

# 16. Final snapshot
arch-chroot /mnt snapper -c root create --description "Post-install baseline" --cleanup-algorithm timeline

echo "=== Installation complete ==="
echo "Reboot and remove install media"
echo "Boot into Lilith OS with passphrase: $PASSPHRASE"