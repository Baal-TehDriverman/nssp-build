#!/bin/bash
# NSSP Lilith OS - Verification script
# Runs after UKI creation to verify the image

set -euo pipefail

echo "=== NSSP Verify: Checking build artifacts ==="

UKI_FILE="../iso/lilith-os-$(uname -m).efi"
ISO_FILE="../iso/lilith-os-$(uname -m).iso"

# Check UKI exists
if [[ -f "$UKI_FILE" ]]; then
    echo "✓ UKI found: $UKI_FILE"
    ls -lh "$UKI_FILE"
    # Verify it's a valid PE file
    file "$UKI_FILE" | grep -q "PE32+ executable" && echo "✓ UKI is valid PE executable" || echo "✗ UKI verification failed"
else
    echo "✗ UKI not found: $UKI_FILE"
    exit 1
fi

# Check ISO exists
if [[ -f "$ISO_FILE" ]]; then
    echo "✓ ISO found: $ISO_FILE"
    ls -lh "$ISO_FILE"
else
    echo "⚠ ISO not found (UKI-only build)"
fi

# Verify UKI contents with objdump if available
if command -v objdump &> /dev/null; then
    echo "=== UKI Sections ==="
    objdump -h "$UKI_FILE" | head -30
fi

# Verify sbctl signature
if command -v sbctl &> /dev/null; then
    echo "=== Secure Boot Verification ==="
    sbctl verify "$UKI_FILE" && echo "✓ UKI signed" || echo "⚠ UKI not signed"
fi

echo "=== Verification complete ==="