#!/bin/bash
# NSSP Lilith OS - Post-install specialized package script
# Runs after the base image is built and repositories are configured

set -euo pipefail

echo "=== NSSP Post-Install: Installing Specialized Packages ==="

# The PreScript already configured chaotic-aur and nvidia repos
# We use pacman --root=/buildroot to install into the image

# Specialized NVIDIA packages
pacman --root=/buildroot --noconfirm -S \
    nvidia \
    nvidia-utils \
    nvidia-settings \
    cuda \
    cudnn \
    nvidia-gpu-exporter

# Chaotic AUR packages
pacman --root=/buildroot --noconfirm -S \
    chaotic-aur/hermes-agent \
    chaotic-aur/lilith-gateway \
    chaotic-aur/cua-driver

# Other specialized tools
pacman --root=/buildroot --noconfirm -S \
    python-pixi \
    lazyvim \
    code \
    zed \
    comfyui \
    ollama \
    vllm \
    llama.cpp \
    whisper.cpp \
    piper \
    manim

echo "=== Specialized Package Installation Complete ==="
