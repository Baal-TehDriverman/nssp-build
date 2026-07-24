# NSSP — Non-Suck Service Provider
## Custom AI Operating System: Lilith OS

**Target Drive:** `/dev/nvme0n1` (500GB, wiped clean)
**User:** tehlappy
**Home:** `/home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD/`

---

## 1. ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LILITH OS (NSSP)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    BARE METAL LAYER                                   │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────────┐   │    │
│  │  │  Linux   │  │  systemd │  │  btrfs   │  │  systemd-boot/     │   │    │
│  │  │  Kernel  │──│  init    │──│  rootfs  │──│  systemd-ukify     │   │    │
│  │  │  6.10+   │  │  (nspawn)│  │  + zstd  │  │  (UKI)             │   │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│  ┌───────────────────────────────────┼───────────────────────────────────┐   │
│  │              SERVICE LAYER (systemd-nspawn / Podman)                   │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────────┐    │   │
│  │  │  Hermes    │ │  ComfyUI   │ │   Ollama   │ │   vLLM / NIM     │    │   │
│  │  │  Gateway   │ │  (GPU)     │ │  (local)   │ │   (NVIDIA NIM)   │    │   │
│  │  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └────────┬─────────┘    │   │
│  │        │              │              │               │                │   │
│  │  ┌─────┴──────────────┴──────────────┴───────────────┴─────────┐    │   │
│  │  │              Lilith Gateway (Port 8080) — Unified API         │    │   │
│  │  │   /v1/chat/completions  /v1/images  /v1/audio  /v1/tools     │    │   │
│  │  └──────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│  ┌───────────────────────────────────┼───────────────────────────────────┐  │
│  │              CONTROL PLANE: LILITH DASHBOARD                           │  │
│  │  /home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD/                        │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │  │
│  │  │  React + Tauri + WebSocket  ←→  Hermes Agent  ←→  Lilith Gateway │   │  │
│  │  │  System Metrics  │  Model Router  │  Tool Orchestrator          │   │  │
│  │  │  Agent Swarm UI  │  Legal War Chest│  Game Dev Pipeline        │   │  │
│  │  │  Crypto/Keys     │  Forensics      │  Media Pipeline           │   │  │
│  │  └─────────────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. BASE OS SPECIFICATION

### 2.1 Kernel & Init
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Kernel** | `linux-zen` 6.10+ | Preemptible, optimized for desktop/AI workloads, NVIDIA patched |
| **Init** | `systemd` (PID 1) + `systemd-nspawn` for containers | Native, declarative, sandboxing built-in |
| **Bootloader** | `systemd-boot` + UKI (Unified Kernel Image) | Secure Boot compatible, atomic updates |
| **Filesystem** | `btrfs` + `zstd:3` compression | Snapshots, subvolumes, compression, send/receive |
| **Initramfs** | `mkinitcpio` with `systemd` hook | Minimal, UKI-compatible |

### 2.2 Partition Layout (nvme0n1 — 500GB)
```
nvme0n1
├─ nvme0n1p1  1GB   vfat       /boot/efi        (ESP, systemd-boot)
├─ nvme0n1p2  32GB  swap       [swap]           (zram fallback)
└─ nvme0n1p3  467GB btrfs      /                (LUKS2 encrypted)
    ├─ @                      →  /               (root)
    ├─ @home                  →  /home           (user data)
    ├─ @snapshots             →  /.snapshots     (snapper)
    ├─ @var_log               →  /var/log
    ├─ @var_cache             →  /var/cache
    ├─ @opt                   →  /opt            (apps, models)
    ├─ @srv                   →  /srv            (services data)
    └─ @lilith                →  /home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD/
```

### 2.3 LUKS2 Encryption
- **Cipher:** `aes-xts-plain64` / `sha256` / 512-bit key
- **PBKDF:** Argon2id, 4 iterations, 1GB RAM, 4 threads
- **Key Slots:** Slot 0 = passphrase "1385", Slot 1 = TPM2 (if available), Slot 2 = recovery key
- **Discard/TRIM:** Enabled (`--allow-discards`)

---

## 3. PACKAGE MANAGEMENT

### 3.1 Primary: `pacman` (Arch base) + `chaotic-aur` + `nvidia` repos
### 3.2 AI/ML Stack: `pixi` (conda-compatible, lockfile-based, reproducible)
### 3.3 Containers: `podman` + `quadlet` (systemd-native, rootless)
### 3.4 Flatpak: User apps (browsers, Discord, Steam)

**Repository Priority:**
```
1. lilith-local      (custom NSSP packages, built from source)
2. chaotic-aur       (prebuilt AUR)
3. nvidia            (NVIDIA drivers, CUDA, NIM)
4. extra/core        (Arch official)
5. flatpak           (user apps)
```

---

## 4. SERVICE LAYER (systemd-nspawn / Podman Quadlet)

### 4.1 Core Services (always running)
| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| `lilith-gateway` | Podman quadlet | 8080 | Unified OpenAI-compatible API |
| `hermes-agent` | systemd-nspawn | 8642 | Hermes Gateway (tools, skills) |
| `ollama` | Podman quadlet | 11434 | Local LLM inference |
| `vllm-nim` | Podman quadlet | 8000 | NVIDIA NIM / vLLM for large models |
| `comfyui` | Podman quadlet (GPU) | 8188 | Image/Video generation |
| `lilith-dashboard` | Native (Tauri) | — | Desktop control plane |

### 4.2 On-Demand Services (socket-activated)
| Service | Trigger | Purpose |
|---------|---------|---------|
| `whisper-api` | `/v1/audio/transcriptions` | STT |
| `tts-api` | `/v1/audio/speech` | TTS |
| `browser-use` | Tool call | Web automation |
| `modal-sandbox` | Tool call | Code execution |
| `fal-queue` | Tool call | Video generation |

---

## 5. LILITH DASHBOARD — ONE FUCKING DASHBOARD

### 5.1 Location
```
/home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD/
├── dashboard/           # Tauri + React + TypeScript app
├── config/              # User config (YAML)
├── data/                # SQLite (metrics, history, sessions)
├── logs/                # Structured logs (JSONL)
├── plugins/             # Dynamic plugin system
├── themes/              # Custom themes (hermes-themes compatible)
└── scripts/             # Automation scripts
```

### 5.2 Tech Stack
| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + TypeScript + Vite + TailwindCSS |
| **Desktop Shell** | Tauri v2 (Rust) — native menus, tray, notifications |
| **Real-time** | WebSocket → Hermes Agent (stdio) + Lilith Gateway (REST) |
| **State** | Zustand + TanStack Query |
| **Charts** | uPlot (metrics), Recharts (analytics) |
| **Terminal** | xterm-rs (PTY) embedded |

### 5.3 Dashboard Panels (Tabs)
```
┌────────────────────────────────────────────────────────────────────────┐
│  🜏 LILITH DASHBOARD                                                    │
├─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬──────────┤
│ SYS │ AI  │ AGT │ DEV │ LGL │ MED │ GAM │ CRY │ NET │ CFG │  TERM    │
│     │     │     │     │     │     │     │     │     │     │          │
│ CPU │Mdl  │Swarm│ Git │ War │ Com │ CP  │ Keys│ VPN │ Sys │  PTY     │
│ GPU │ Rtr │ Logs│ CI  │ Chst│fyUI │2077 │ Wlt │ SSH │ Env │  Shell   │
│ RAM │Inf  │Chrt │ PKG │ Evd │ Vid │ Mod │ NFT │ FW  │ Keys│  Logs    │
│ DISK│Tkn  │Dlgt │Dep  │Med  │Aud  │SDK  │Min  │DNS  │Bak  │  AI      │
│ NET │Cst  │Skil │Tst  │For  │Gen  │Dpl  │Stk  │Mon  │Upd  │  Chat    │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴──────────┘
```

### 5.4 Panel Specifications

| Panel | Key Features | Backend Integration |
|-------|-------------|---------------------|
| **SYS** | Real-time GPU/CPU/RAM/Disk/Net, sensors, thermal, NVIDIA-SMI | `collectd` + `nvml` + WebSocket |
| **AI** | Model router (local/remote), token usage, cost tracking, benchmark | Lilith Gateway `/v1/models`, `/v1/usage` |
| **AGT** | Agent swarm visualizer, delegation graph, live logs, session replay | Hermes `delegate_task`, `session_search` |
| **DEV** | Git worktree manager, CI status, pkg updates, container logs | `gh`, `podman`, `pacman`, `pixi` APIs |
| **LGL** | War Chest browser, evidence timeline, Himalaya email, case tracker | `himalaya`, `war-chest` skill, SQLite |
| **MED** | ComfyUI workflow gallery, video queue, audio studio, asset library | ComfyUI API, `heartmula`, `songsee` |
| **GAM** | CP2077 mod manager, Redscript deploy, MSN wave visualizer | `cyberpunk-deployment-automation`, `blackspace-engine-modding` |
| **CRY** | Hardware wallet UI, key derivation, TX builder, portfolio | `hw-cli`, `bitcoin-cli`, `ethers-rs` |
| **NET** | WireGuard/Tailscale/SSH manager, port forward, DNS, traffic graph | `wg`, `tailscale`, `nftables`, `vnstat` |
| **CFG** | Dotfiles sync, secrets vault, system updates, backup/restore | `chezmoi`, `age`, `snapper`, `timeshift` |
| **TERM** | Embedded PTY with AI sidebar, command history, agent chat | `xterm-rs`, Hermes stdio |

---

## 6. PREBUILT TOOL STACK

### 6.1 AI/ML Infrastructure
| Tool | Version | Deployment | GPU |
|------|---------|------------|-----|
| Ollama | 0.30+ | Podman quadlet | ✓ |
| vLLM | 0.6+ | Podman quadlet (NIM) | ✓ |
| NVIDIA NIM | Latest | Podman quadlet | ✓ |
| ComfyUI | Latest | Podman quadlet (GPU) | ✓ |
| Whisper.cpp | Latest | Socket-activated | ✓ |
| Piper TTS | Latest | Socket-activated | ✓ |
| Llama.cpp | Latest | Native (AVX2/AMX) | CPU |

### 6.2 Development Environment
| Category | Tools |
|----------|-------|
| **Editors** | Neovim (LazyVim), VS Code (Flatpak), Zed |
| **CLI** | fish (default), zsh, nushell, atuin, fzf, ripgrep, fd, bat, eza, delta |
| **Git** | gh, gitui, lazygit, git-absorb, git-delta, worktree-manager |
| **Containers** | podman, buildah, skopeo, quadlet, compose (podman-compose) |
| **CI/CD** | act (local GitHub Actions), woodpecker, drone |
| **Languages** | Rust (rustup), Go, Python (pixi/uv), Node (fnm), Bun, Zig, Odin |
| **AI Coding** | Hermes Agent, Codex CLI, Claude Code, OpenCode, Aider |

### 6.3 Infrastructure & Operations
| Tool | Purpose |
|------|---------|
| `systemd` + `systemd-nspawn` | Service orchestration, sandboxing |
| `podman` + `quadlet` | Rootless containers, systemd integration |
| `tailscale` + `wireguard` | Mesh VPN, exit nodes |
| `nftables` + `firewalld` | Firewall, port forwarding |
| `prometheus` + `grafana` | Metrics (node-exporter, nvidia-gpu-exporter) |
| `vector` / `loki` | Log aggregation |
| `restic` + `rclone` | Encrypted backups (B2, R2, local) |
| `snapper` + `btrfs` | System snapshots, rollback |
| `age` / `sops` | Secrets encryption |
| `chezmoi` | Dotfiles management |

### 6.4 Legal / Forensics / War Chest
| Tool | Purpose |
|------|---------|
| `himalaya` | IMAP/SMTP email (terminal) |
| `war-chest` skill | Evidence aggregation, campaign management |
| `legal-medical-evidence-verification` | Case file verification |
| `forensic-asset-recovery` | Code/data recovery from fragmented sources |
| `case-fact-verification-workflow` | Systematic fact-checking |

### 6.5 Media & Creative
| Tool | Purpose |
|------|---------|
| ComfyUI + custom nodes | Image/video/audio generation |
| `heartmula` | Suno-style music from lyrics |
| `songsee` | Audio analysis (spectrograms, MFCC) |
| `manim` | Mathematical animations |
| `p5.js` / `touchdesigner` | Generative art, shaders |
| `ffmpeg` + `yt-dlp` | Video processing, downloading |

### 6.6 Game Development (Cyberpunk 2077 / BlackSpace)
| Tool | Purpose |
|------|---------|
| `cyberpunk-deployment-automation` | Mod deployment pipeline |
| `blackspace-engine-modding` | Engine modification |
| `lightsaber-vfx-system` | VFX implementation |
| `msn-deployment-verifier` | MSN mod verification |
| `redscript` toolchain | Compile/deploy REDscript |

---

## 7. BUILD PIPELINE

### 7.1 Repository Structure
```
nssp-os/
├── config/
│   ├── packages.x86_64        # Base packages
│   ├── packages.ai.x86_64     # AI/ML packages
│   ├── packages.dev.x86_64    # Dev packages
│   ├── packages.media.x86_64  # Media packages
│   └── packages.legal.x86_64  # Legal/forensics
├── overlays/
│   ├── etc/                   # /etc overlay
│   ├── usr/                   # /usr overlay
│   └── home/                  # /home/tehlappy overlay
├── systemd/
│   ├── *.service              # System services
│   ├── *.socket               # Socket activation
│   └── *.conf                 # Drop-ins
├── quadlets/
│   ├── *.container            # Podman quadlets
│   ├── *.network              # Podman networks
│   └── *.volume               # Podman volumes
├── scripts/
│   ├── build-iso.sh           # ISO builder (mkosi)
│   ├── build-uki.sh           # UKI builder (ukiify)
│   ├── install.sh             # Installer (archinstall-based)
│   └── post-install.sh        # First-boot configuration
├── keys/
│   ├── lilith-pub.pem         # Repo signing key
│   └── sops-age.txt           # SOPS age key
├── lilith-dashboard/          # Tauri app source
└── nssp.spec.md               # This file
```

### 7.2 Build Tools
| Tool | Purpose |
|------|---------|
| `mkosi` | Build reproducible disk images / UKIs |
| `ukiify` | Unified Kernel Image generation |
| `archinstall` | Automated installation |
| `systemd-repart` | Partition management |
| `sbctl` | Secure Boot key enrollment |
| `cosign` + `fulcio` | Container/image signing |

### 7.3 Artifacts Produced
| Artifact | Format | Use Case |
|----------|--------|----------|
| `lilith-os-uki.efi` | UKI (PE) | Direct boot, Secure Boot |
| `lilith-os.iso` | ISO 9660 | USB install, VM |
| `lilith-os.raw.zst` | Compressed disk image | `dd` to NVMe, PXE |
| `lilith-os.qcow2` | QCOW2 | QEMU/libvirt VM |

---

## 8. DEPLOYMENT TO nvme0n1 (500GB)

### 8.1 One-Shot Install Script
```bash
#!/usr/bin/env bash
# run as root from live ISO
set -euo pipefail

DISK="/dev/nvme0n1"
PASSPHRASE="1385"
HOSTNAME="lilith"
USERNAME="tehlappy"

# 1. Partition
sgdisk -Z "$DISK"
sgdisk -n 1:0:+1G   -t 1:ef00 -c 1:"EFI"      "$DISK"
sgdisk -n 2:0:+32G  -t 2:8200 -c 2:"SWAP"     "$DISK"
sgdisk -n 3:0:0     -t 3:8300 -c 3:"ROOT"     "$DISK"
partprobe "$DISK"

# 2. LUKS2 on root
echo -n "$PASSPHRASE" | cryptsetup luksFormat --type luks2 \
  --cipher aes-xts-plain64 --hash sha256 --key-size 512 \
  --pbkdf argon2id --iter-time 4000 --pbkdf-memory 1048576 --pbkdf-parallel 4 \
  "${DISK}p3" -
echo -n "$PASSPHRASE" | cryptsetup open "${DISK}p3" cryptroot -

# 3. Btrfs with subvolumes
mkfs.btrfs -L LILITH_ROOT /dev/mapper/cryptroot
mount /dev/mapper/cryptroot /mnt
for sv in @ @home @snapshots @var_log @var_cache @opt @srv @lilith; do
  btrfs su cr /mnt/$sv
done
umount /mnt

# 4. Mount for install
mount -o subvol=@,compress=zstd:3,noatime /dev/mapper/cryptroot /mnt
mkdir -p /mnt/{boot/efi,home,.snapshots,var/log,var/cache,opt,srv}
mkdir -p "/mnt/home/$USERNAME/🜏 Lilith/ONE FUCKING DASHBOARD"
mount -o subvol=@home,compress=zstd:3,noatime /dev/mapper/cryptroot /mnt/home
mount -o subvol=@snapshots,compress=zstd:3,noatime /dev/mapper/cryptroot /mnt/.snapshots
mount -o subvol=@var_log,compress=zstd:3,noatime /dev/mapper/cryptroot /mnt/var/log
mount -o subvol=@var_cache,compress=zstd:3,noatime /dev/mapper/cryptroot /mnt/var/cache
mount -o subvol=@opt,compress=zstd:3,noatime /dev/mapper/cryptroot /mnt/opt
mount -o subvol=@srv,compress=zstd:3,noatime /dev/mapper/cryptroot /mnt/srv
mount -o subvol=@lilith,compress=zstd:3,noatime /dev/mapper/cryptroot "/mnt/home/$USERNAME/🜏 Lilith/ONE FUCKING DASHBOARD"
mkfs.vfat -F32 "${DISK}p1" && mount "${DISK}p1" /mnt/boot/efi
mkswap "${DISK}p2" && swapon "${DISK}p2"

# 5. Base install
pacstrap -K /mnt base linux-zen linux-zen-headers btrfs-progs \
  systemd systemd-ukify mkinitcpio networkmanager \
  sudo fish git age sops chezmoi snapper

# 6. Generate fstab, crypttab, ukify config
genfstab -U /mnt >> /mnt/etc/fstab
echo "cryptroot UUID=$(blkid -s UUID -o value ${DISK}p3) none luks,discard" > /mnt/etc/crypttab.initramfs

# 7. UKI + systemd-boot
arch-chroot /mnt bootctl install
arch-chroot /mnt kernel-install add "$(pacman -Q linux-zen | cut -d' ' -f2)" /boot

# 8. Copy overlay, run post-install
rsync -a overlays/ /mnt/
arch-chroot /mnt /scripts/post-install.sh

# 9. Sign UKI for Secure Boot (if enrolled)
# sbctl sign -s /mnt/boot/EFI/Linux/lilith-os.efi
```

### 8.2 Post-Install (runs in chroot)
- Create user `tehlappy`, add to `wheel,kvm,render,video,docker,libvirt`
- Enable services: `NetworkManager`, `systemd-resolved`, `systemd-timesyncd`, `fstrim.timer`, `snapper-timeline.timer`, `snapper-cleanup.timer`
- Install `lilith-dashboard` (Tauri app) to `~/.local/bin`
- Deploy quadlets to `/etc/containers/systemd/`
- Run `chezmoi apply` for dotfiles
- Enroll Secure Boot keys (`sbctl enroll-keys`)

---

## 9. SECURITY MODEL

| Layer | Mechanism |
|-------|-----------|
| **Boot** | Secure Boot (Microsoft + custom keys), UKI signed, TPM2 measured boot |
| **Disk** | LUKS2 + Argon2id, TPM2 auto-unlock (optional), discard/TRIM |
| **Runtime** | systemd-nspawn (namespace isolation), Podman rootless, SECCOMP profiles |
| **Secrets** | `age` + `sops` for files, `systemd-creds` for services, TPM2 for keys |
| **Network** | nftables default-deny, Tailscale/WireGuard for remote, no exposed ports |
| **Updates** | Automatic snapshots pre-update, `pacman` hooks, `mkosi` reproducible builds |

---

## 10. ROADMAP

### Phase 1: Foundation (Week 1-2)
- [ ] Build UKI + ISO with `mkosi`
- [ ] Install to nvme0n1, verify boot, encryption, snapshots
- [ ] Deploy core services: lilith-gateway, ollama, hermes-agent
- [ ] Basic Lilith Dashboard (Tauri shell + SYS panel)

### Phase 2: AI Stack (Week 3-4)
- [ ] vLLM/NIM deployment for nemotron-3-ultra
- [ ] ComfyUI + custom nodes (GPU container)
- [ ] Model router in Lilith Gateway (local ↔ cloud)
- [ ] AI panel: model mgmt, token tracking, benchmarks

### Phase 3: Agent Swarm (Week 5-6)
- [ ] Hermes skills: all current + NSSP-specific
- [ ] Agent panel: delegation graph, session replay, live logs
- [ ] Lilith Knowledge Integration (LilithData.txt, Training Data.txt)
- [ ] Sovereign-Core agents integrated via dashboard

### Phase 4: Domain Panels (Week 7-10)
- [ ] DEV panel: git worktrees, CI, containers, pkg mgmt
- [ ] LGL panel: War Chest, Himalaya, evidence timeline
- [ ] MED panel: ComfyUI gallery, video queue, audio studio
- [ ] GAM panel: CP2077 mod pipeline, BlackSpace, MSN waves
- [ ] CRY panel: HW wallet, keys, portfolio
- [ ] NET panel: VPN, firewall, DNS, traffic

### Phase 5: Polish (Week 11-12)
- [ ] Themes (hermes-themes compatible)
- [ ] Plugin SDK for dashboard
- [ ] Backup/restore one-click
- [ ] Documentation, installable ISO release

---

## 11. REPOSITORY & DOTFILES INTEGRATION

```bash
# After first boot:
chezmoi init --apply git@github.com:tehlappy/lilith-dotfiles.git

# Dotfiles repo structure:
lilith-dotfiles/
├── .config/
│   ├── fish/
│   ├── hermes/
│   ├── lilith-dashboard/
│   ├── systemd/user/
│   └── containers/systemd/
├── .local/bin/
│   ├── lilith-dashboard
│   ├── nssp-*
│   └── herm
├── .age/identity.age       # SOPS/age private key (encrypted)
└── README.md
```

---

## 12. COMMANDS CHEATSHEET

```bash
# System
nssp-update          # Full system update + snapshot
nssp-rollback        # Snapper rollback menu
nssp-backup          # Restic backup to B2/R2
nssp-restore         # Restore from backup

# AI
lilith-models        # List/pull/remove models (ollama/vllm/nim)
lilith-bench         # Benchmark models
lilith-cost          # Token cost tracker

# Dashboard
lilith-dashboard     # Launch dashboard (Tauri)
lilith-dashboard --tray  # Background tray mode

# Containers
podman-systemd       # Manage quadlet services
nssp-logs <service>  # Structured logs (journalctl + vector)

# Legal
war-chest            # Open War Chest TUI
himalaya             # Email client
```

---

**END OF SPEC** — Ready for implementation on `/dev/nvme0n1`.