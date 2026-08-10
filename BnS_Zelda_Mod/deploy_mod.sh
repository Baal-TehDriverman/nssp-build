#!/bin/bash
# Rock-solid per-file mod deployer (fix: < /dev/null so adb push doesn't eat the loop's stdin).
# Usage: deploy_mod <serial> <src_mod_dir> <dest_parent> <modname>
set -e
S="$1"; SRC="$2"; DEST_PARENT="$3"; NAME="$4"
DEST="$DEST_PARENT/$NAME"
adb -s $S shell "mkdir -p '$DEST'"

# Build file path list into a temp file
TMPLIST=$(mktemp)
(cd "$SRC" && find . -type f \( -name '*.json' -o -name '*.dll' -o -name '*.cs' -o -name '*.png' -o -name 'id.modio' \)) > "$TMPLIST"

count=0
while IFS= read -r rel <&3; do
    [ -z "$rel" ] && continue
    rel="${rel#./}"
    dir=$(dirname "$rel")
    [ "$dir" = "." ] && dir=""
    full="$SRC/$rel"
    if [ -n "$dir" ]; then
        adb -s $S shell "mkdir -p '$DEST/$dir'" < /dev/null 2>/dev/null
        adb -s $S push "$full" "$DEST/$dir/" < /dev/null >/dev/null 2>&1 || echo "FAIL: $rel"
    else
        adb -s $S push "$full" "$DEST/" < /dev/null >/dev/null 2>&1 || echo "FAIL: $rel"
    fi
    count=$((count+1))
done 3< "$TMPLIST"
rm -f "$TMPLIST"
echo "  deployed $count files -> $DEST"