#!/bin/bash
# NSSP Lilith OS - mkosi build configuration
# Run from nssp-build/ directory

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../iso"

mkdir -p "$OUTPUT_DIR"

echo "=== Building NSSP Lilith OS UKI ==="

# Build UKI
mkosi build \
  --format uki \
  --output-dir "$OUTPUT_DIR" \
  --output lilith-os-uki \
  --kernel linux-zen \
  --kernel-command-line "root=LABEL=LILITH_ROOT rootflags=subvol=@,compress=zstd:3,noatime rw quiet loglevel=3 systemd.show_status=auto rd.udev.log_level=3" \
  --distribution arch \
  --release rolling \
  --architecture x86-64 \
  --package base \
  --package linux-zen \
  --package linux-zen-headers \
  --package linux-firmware \
  --package btrfs-progs \
  --package cryptsetup \
  --package systemd \
  --package systemd-ukify \
  --package mkinitcpio \
  --package networkmanager \
  --package sudo \
  --package fish \
  --package git \
  --package age \
  --package sops \
  --package chezmoi \
  --package snapper \
  --package grub \
  --package efibootmgr \
  --package sbctl \
  --package nvidia \
  --package nvidia-utils \
  --package nvidia-settings \
  --package cuda \
  --package cudnn \
  --package podman \
  --package buildah \
  --package skopeo \
  --package containerd \
  --package docker-compose \
  --package python \
  --package python-pip \
  --package python-pixi \
  --package rustup \
  --package go \
  --package nodejs \
  --package npm \
  --package bun \
  --package zig \
  --package neovim \
  --package lazyvim \
  --package code \
  --package zed \
  --package fzf \
  --package ripgrep \
  --package fd \
  --package bat \
  --package eza \
  --package delta \
  --package atuin \
  --package lazygit \
  --package gitui \
  --package gh \
  --package tailscale \
  --package wireguard-tools \
  --package nftables \
  --package firewalld \
  --package prometheus \
  --package grafana \
  --package node-exporter \
  --package nvidia-gpu-exporter \
  --package vector \
  --package loki \
  --package restic \
  --package rclone \
  --package snapper \
  --package timeshift \
  --package himalaya \
  --package ffmpeg \
  --package yt-dlp \
  --package imagemagick \
  --package manim \
  --package blender \
  --package obs-studio \
  --package comfyui \
  --package ollama \
  --package vllm \
  --package llama.cpp \
  --package whisper.cpp \
  --package piper \
  --package "chaotic-aur/hermes-agent" \
  --package "chaotic-aur/lilith-gateway" \
  --package "chaotic-aur/cua-driver" \
  --preset auto \
  --bootable yes \
  --bootloader systemd-boot \
  --uefi yes \
  --secure-boot yes \
  --partition-table gpt \
  --size 500G \
  --overlay "$SCRIPT_DIR/../overlays" \
  --scripts "$SCRIPT_DIR" \
  --pre-script prepare.sh \
  --post-script verify.sh \
  --environment LANG=en_US.UTF-8 \
  --environment LC_ALL=en_US.UTF-8 \
  --environment TZ=America/Los_Angeles \
  --hostname lilith \
  --user tehlappy \
  --password 1385 \
  --default-shell /usr/bin/fish \
  --timezone America/Los_Angeles \
  --locale en_US.UTF-8 \
  --keyboard us

# Rename UKI to expected name
UKI_GENERATED="$OUTPUT_DIR/lilith-os-uki.uki"
UKI_EXPECTED="$OUTPUT_DIR/lilith-os-$(uname -m).efi"
if [[ -f "$UKI_GENERATED" ]]; then
  mv "$UKI_GENERATED" "$UKI_EXPECTED"
  echo "Renamed UKI to $UKI_EXPECTED"
else
  echo "UKI file not found: $UKI_GENERATED"
  # Sometimes the extension is .uki, sometimes it's just the output name without extension?
  # Let's check for the output name directly
  UKI_ALT="$OUTPUT_DIR/lilith-os-uki"
  if [[ -f "$UKI_ALT" ]]; then
    mv "$UKI_ALT" "$UKI_EXPECTED"
    echo "Renamed UKI (alternative) to $UKI_EXPECTED"
  else
    # List what we have in the output directory for debugging
    echo "Files in $OUTPUT_DIR:"
    ls -la "$OUTPUT_DIR"
    exit 1
  fi
fi

echo "=== Building NSSP Lilith OS ISO (disk image) ==="

# Build disk image (ISO)
mkosi build \
  --format disk \
  --output-dir "$OUTPUT_DIR" \
  --output lilith-os-disk \
  --kernel linux-zen \
  --kernel-command-line "root=LABEL=LILITH_ROOT rootflags=subvol=@,compress=zstd:3,noatime rw quiet loglevel=3 systemd.show_status=auto rd.udev.log_level=3" \
  --distribution arch \
  --release rolling \
  --architecture x86-64 \
  --package base \
  --package linux-zen \
  --package linux-zen-headers \
  --package linux-firmware \
  --package btrfs-progs \
  --package cryptsetup \
  --package systemd \
  --package systemd-ukify \
  --package mkinitcpio \
  --package networkmanager \
  --package sudo \
  --package fish \
  --package git \
  --package age \
  --package sops \
  --package chezmoi \
  --package snapper \
  --package grub \
  --package efibootmgr \
  --package sbctl \
  --package nvidia \
  --package nvidia-utils \
  --package nvidia-settings \
  --package cuda \
  --package cudnn \
  --package podman \
  --package buildah \
  --package skopeo \
  --package containerd \
  --package docker-compose \
  --package python \
  --package python-pip \
  --package python-pixi \
  --package rustup \
  --package go \
  --package nodejs \
  --package npm \
  --package bun \
  --package zig \
  --package neovim \
  --package lazyvim \
  --package code \
  --package zed \
  --package fzf \
  --package ripgrep \
  --package fd \
  --package bat \
  --package eza \
  --package delta \
  --package atuin \
  --package lazygit \
  --package gitui \
  --package gh \
  --package tailscale \
  --package wireguard-tools \
  --package nftables \
  --package firewalld \
  --package prometheus \
  --package grafana \
  --package node-exporter \
  --package nvidia-gpu-exporter \
  --package vector \
  --package loki \
  --package restic \
  --package rclone \
  --package snapper \
  --package timeshift \
  --package himalaya \
  --package ffmpeg \
  --package yt-dlp \
  --package imagemagick \
  --package manim \
  --package blender \
  --package obs-studio \
  --package comfyui \
  --package ollama \
  --package vllm \
  --package llama.cpp \
  --package whisper.cpp \
  --package piper \
  --package "chaotic-aur/hermes-agent" \
  --package "chaotic-aur/lilith-gateway" \
  --package "chaotic-aur/cua-driver" \
  --preset auto \
  --bootable yes \
  --bootloader systemd-boot \
  --uefi yes \
  --secure-boot yes \
  --partition-table gpt \
  --size 500G \
  --overlay "$SCRIPT_DIR/../overlays" \
  --scripts "$SCRIPT_DIR" \
  --pre-script prepare.sh \
  --post-script verify.sh \
  --environment LANG=en_US.UTF-8 \
  --environment LC_ALL=en_US.UTF-8 \
  --environment TZ=America/Los_Angeles \
  --hostname lilith \
  --user tehlappy \
  --password 1385 \
  --default-shell /usr/bin/fish \
  --timezone America/Los_Angeles \
  --locale en_US.UTF-8 \
  --keyboard us

# Rename disk image to expected ISO name
ISO_GENERATED="$OUTPUT_DIR/lilith-os-disk.disk"
ISO_EXPECTED="$OUTPUT_DIR/lilith-os-$(uname -m).iso"
if [[ -f "$ISO_GENERATED" ]]; then
  mv "$ISO_GENERATED" "$ISO_EXPECTED"
  echo "Renamed ISO to $ISO_EXPECTED"
else
  echo "ISO file not found: $ISO_GENERATED"
  # Check for alternative naming
  ISO_ALT="$OUTPUT_DIR/lilith-os-disk"
  if [[ -f "$ISO_ALT" ]]; then
    mv "$ISO_ALT" "$ISO_EXPECTED"
    echo "Renamed ISO (alternative) to $ISO_EXPECTED"
  else
    # List what we have in the output directory for debugging
    echo "Files in $OUTPUT_DIR:"
    ls -la "$OUTPUT_DIR"
    exit 1
  fi
fi

echo "=== Build complete ==="
echo "Artifacts in: $OUTPUT_DIR"
ls -lh "$OUTPUT_DIR"