#!/usr/bin/env bash
BT_BACKUP_DIR="${1:-$HOME/.local/share/data/qBittorrent/BT_backup}"

VALID_FILE=$(find "$BT_BACKUP_DIR" -name '*.fastresume' -size +1c -print -quit)
find "$BT_BACKUP_DIR" -name '*.fastresume' -size 0 -exec cp "${VALID_FILE}" "{}" \;

