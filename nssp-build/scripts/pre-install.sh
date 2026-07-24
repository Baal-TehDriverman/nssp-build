#!/bin/bash
# NSSP Lilith OS - Pre-install script
# Runs inside the build container before package installation

set -euo pipefail

echo "=== NSSP Pre-Install: Setting up build environment ==="

# Configure mkinitcpio for UKI + btrfs + luks + zstd
cat > /etc/mkinitcpio.conf.d/nssp.conf << 'EOF'
MODULES=(btrfs nvidia nvidia_modeset nvidia_uvm nvidia_drm)
BINARIES=(/usr/bin/btrfs /usr/sbin/cryptsetup)
FILES=()
HOOKS=(base systemd autodetect microcode modconf kms keyboard keymap consolefont block encrypt btrfs filesystems fsck)
COMPRESSION="zstd"
COMPRESSION_OPTIONS=(-3)
EOF

# Configure zram for swap
cat > /etc/systemd/zram-generator.conf << 'EOF'
[zram0]
zram-size = min(ram, 32G)
compression-algorithm = zstd
swap-priority = 100
EOF

# Configure pacman for chaotic-aur and nvidia repos
cat >> /etc/pacman.conf << 'EOF'

[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist

[nvidia]
Server = https://pkgbuild.com/~dreamsalad/nvidia/\$arch
EOF

# Install chaotic-aur keyring
pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
pacman-key --lsign-key 3056513887B78AEB
pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'

echo "=== Pre-install complete ==="