#!/usr/bin/env bash
BT_BACKUP_DIR="${1:-$HOME/.local/share/data/qBittorrent/BT_backup}"

if [ ! -d "$BT_BACKUP_DIR" ]; then
  echo "$BT_BACKUP_DIR not found, exiting"
  exit 1
fi

VALID_FILE=$(find "$BT_BACKUP_DIR" -name '*.fastresume' -size +1c -print -quit)
find "$BT_BACKUP_DIR" -name '*.fastresume' -size 0 -exec cp "${VALID_FILE}" "{}" \;

