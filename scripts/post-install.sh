#!/bin/bash
# NSSP Lilith OS - Post-install script
# Runs after package installation, inside the image

set -euo pipefail

echo "=== NSSP Post-Install: Configuring Lilith OS ==="

# Create user
useradd -m -G wheel,video,render,input -s /usr/bin/fish tehlappy
echo "tehlappy:1385" | chpasswd
echo "root:1385" | chpasswd

# Sudo without password for wheel
echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel

# Hostname
echo "lilith" > /etc/hostname
cat > /etc/hosts << 'EOF'
127.0.0.1   localhost
::1         localhost
127.0.1.1   lilith.localdomain lilith
EOF

# Locale
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Timezone
ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
hwclock --systohc

# NetworkManager
systemctl enable NetworkManager

# btrfs subvolumes will be created on first boot via systemd-tmpfiles
cat > /etc/tmpfiles.d/nssp-btrfs.conf << 'EOF'
d /home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD 0755 tehlappy tehlappy -
d /opt/ai-models 0755 tehlappy tehlappy -
d /opt/nssp 0755 root root -
d /srv/lilith 0755 tehlappy tehlappy -
EOF

# Enable services
systemctl enable systemd-timesyncd
systemctl enable fstrim.timer
systemctl enable paccache.timer
systemctl enable snapper-timeline.timer
systemctl enable snapper-cleanup.timer
systemctl enable btrfs-scrub@-.timer
systemctl enable zram-generator

# NVIDIA
systemctl enable nvidia-suspend nvidia-hibernate nvidia-resume

# Ollama
systemctl enable ollama

# Podman socket for rootless containers
systemctl enable --user podman.socket

# Flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Configure mkinitcpio for UKI
mkinitcpio -P

# Setup secure boot keys (will enroll on first boot)
sbctl create-keys
sbctl enroll-keys -m

echo "=== Post-install complete ==="