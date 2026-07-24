#!/bin/bash
# NSSP Lilith OS - First boot configuration
# Runs on first boot via systemd service

set -euo pipefail

echo "=== NSSP First Boot Configuration ==="

# Wait for network
systemctl wait network-online.target --timeout=30

# Enroll Secure Boot keys if not enrolled
if ! sbctl verify /boot/EFI/Linux/lilith-os.efi 2>/dev/null; then
    echo "Enrolling Secure Boot keys..."
    sbctl enroll-keys -m || true
fi

# Setup TPM2 auto-unlock for LUKS (if TPM2 available)
if command -v systemd-cryptenroll &> /dev/null && [[ -c /dev/tpmrm0 ]]; then
    echo "Enrolling TPM2 for LUKS auto-unlock..."
    systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=0+7 /dev/nvme0n1p3 || true
fi

# Start and enable Podman for user
systemctl --user enable --now podman.socket

# Pull and start core containers
podman pull ghcr.io/lilith-systems/lilith-gateway:latest || true
podman pull ollama/ollama:latest || true
podman pull nvcr.io/nim/nvidia/nemotron-3-ultra:latest || true
podman pull comfyui/comfyui:latest-gpu || true

# Start services
systemctl --user start lilith-gateway.service || true
systemctl start ollama.service || true

# Setup chezmoi for dotfiles
if [[ -d /home/tehlappy/.local/share/chezmoi ]]; then
    cd /home/tehlappy
    sudo -u tehlappy chezmoi apply || true
fi

# Initialize Lilith Dashboard data directories
mkdir -p "/home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD"/{data,logs,plugins,themes}
chown -R tehlappy:tehlappy "/home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD"

# Initialize snapper configs if not done
snapper -c root create-config / 2>/dev/null || true
snapper -c home create-config /home 2>/dev/null || true

# Create initial snapshots
snapper -c root create --description "First boot baseline" --cleanup-algorithm timeline
snapper -c home create --description "First boot baseline" --cleanup-algorithm timeline

# Setup Himalaya email config template
mkdir -p /home/tehlappy/.config/himalaya
cat > /home/tehlappy/.config/himalaya/config.toml << 'EOF'
[account.default]
backend = "imap"
download-dir = "/home/tehlappy/Mail"
imap-host = "imap.gmail.com"
imap-port = 993
imap-username = "ericmathewhill@gmail.com"
imap-password = "env:HIMALAYA_IMAP_PASSWORD"
smtp-host = "smtp.gmail.com"
smtp-port = 587
smtp-username = "ericmathewhill@gmail.com"
smtp-password = "env:HIMALAYA_SMTP_PASSWORD"
smtp-starttls = true
EOF
chown -R tehlappy:tehlappy /home/tehlappy/.config/himalaya

# Setup age/sops for secrets
if [[ ! -f /home/tehlappy/.age/identity.age ]]; then
    mkdir -p /home/tehlappy/.age
    sudo -u tehlappy age-keygen -o /home/tehlappy/.age/identity.age
fi

# Mark first boot complete
touch /var/lib/nssp-first-boot-complete

echo "=== First boot configuration complete ==="