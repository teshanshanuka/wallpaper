#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0))
IMG=$($THIS_DIR/venv/bin/python $THIS_DIR/main.py "${HOME}/Pictures/wallpapers")

[ $? -ne 0 ] && { echo "main.py failed: ${IMG}" >&2; exit 1; }

echo "Downloaded $IMG"
ln -sf "${IMG}" "${HOME}/Pictures/wallpapers/wallpaper.png"
