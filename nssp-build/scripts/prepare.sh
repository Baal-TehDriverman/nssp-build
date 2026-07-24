#!/bin/bash
# NSSP Lilith OS - Prepare script
# Runs after image is built, before UKI creation

set -euo pipefail

echo "=== NSSP Prepare: Final image preparation ==="

# Copy custom systemd units
mkdir -p /etc/systemd/system/
cp -r /usr/lib/systemd/system/*.service /etc/systemd/system/ 2>/dev/null || true

# Copy quadlet files for Podman services
mkdir -p /etc/containers/systemd/
cat > /etc/containers/systemd/lilith-gateway.container << 'EOF'
[Unit]
Description=Lilith Gateway - Unified AI API
After=network-online.target
Wants=network-online.target

[Container]
Image=ghcr.io/lilith-systems/lilith-gateway:latest
AutoUpdate=registry
PublishPort=8080:8080
Volume=/home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD:/data:Z
Volume=/opt/ai-models:/models:ro,Z
Environment=LILITH_CONFIG=/data/config/gateway.yaml
Environment=MODEL_CACHE_DIR=/models
ExecStart=/usr/local/bin/lilith-gateway
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

cat > /etc/containers/systemd/ollama.container << 'EOF'
[Unit]
Description=Ollama Local LLM Server
After=network-online.target
Wants=network-online.target

[Container]
Image=ollama/ollama:latest
AutoUpdate=registry
PublishPort=11434:11434
Volume=/opt/ai-models/ollama:/root/.ollama:Z
Environment=OLLAMA_HOST=0.0.0.0
Environment=OLLAMA_NUM_PARALLEL=4
Environment=OLLAMA_MAX_LOADED_MODELS=3
ExecStart=/bin/ollama serve
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

cat > /etc/containers/systemd/vllm-nim.container << 'EOF'
[Unit]
Description=vLLM / NVIDIA NIM Inference Server
After=network-online.target
Wants=network-online.target
Requires=nvidia-container-toolkit.service

[Container]
Image=nvcr.io/nim/nvidia/nemotron-3-ultra:latest
AutoUpdate=registry
PublishPort=8000:8000
Volume=/opt/ai-models/nim:/opt/nim:Z
Environment=NGC_API_KEY=${NGC_API_KEY}
Environment=NIM_MODEL_NAME=nemotron-3-ultra
Environment=NIM_HTTP_PORT=8000
Device=nvidia.com/gpu=all
SecurityLabel=disable
ExecStart=/opt/nim/entrypoint.sh
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

cat > /etc/containers/systemd/comfyui.container << 'EOF'
[Unit]
Description=ComfyUI Image/Video Generation
After=network-online.target
Wants=network-online.target
Requires=nvidia-container-toolkit.service

[Container]
Image=comfyui/comfyui:latest-gpu
AutoUpdate=registry
PublishPort=8188:8188
Volume=/opt/ai-models/comfyui:/comfyui/models:Z
Volume=/home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD/output:/comfyui/output:Z
Device=nvidia.com/gpu=all
SecurityLabel=disable
ShmSize=8G
ExecStart=python main.py --listen 0.0.0.0 --port 8188
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# Systemd user services for Hermes
mkdir -p /etc/systemd/user/
cat > /etc/systemd/user/hermes-gateway.service << 'EOF'
[Unit]
Description=Hermes Agent Gateway
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=exec
Environment=HERMES_CONFIG_DIR=%h/.hermes
Environment=HERMES_ENV_FILE=%h/.hermes/.env
ExecStart=%h/.local/bin/hermes gateway run
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF

# Enable user services globally
systemctl --global enable hermes-gateway.service
systemctl --global enable podman.socket

# Configure Lilith Gateway config template
mkdir -p /home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD/config
cat > /home/tehlappy/🜏 Lilith/ONE FUCKING DASHBOARD/config/gateway.yaml << 'EOF'
# Lilith Gateway Configuration
server:
  host: "0.0.0.0"
  port: 8080
  workers: 4

models:
  local:
    provider: "ollama"
    base_url: "http://localhost:11434/v1"
    models:
      - "nemotron-3-ultra:local"
      - "qwen3-coder:latest"
      - "llama3.3:latest"
  cloud:
    provider: "nvidia-nim"
    base_url: "http://localhost:8000/v1"
    models:
      - "nvidia/nemotron-3-ultra-550b-a55b"
  comfyui:
    provider: "comfyui"
    base_url: "http://localhost:8188"

routing:
  default: "local"
  fallback: "cloud"
  rules:
    - pattern: "code|reasoning"
      target: "cloud"
    - pattern: "image|video|audio"
      target: "comfyui"

auth:
  enabled: false
  api_keys: []

logging:
  level: "info"
  format: "json"
  output: "stdout"

metrics:
  enabled: true
  port: 9090
EOF

# Fix ownership
chown -R 1000:1000 /home/tehlappy

echo "=== Prepare complete ==="