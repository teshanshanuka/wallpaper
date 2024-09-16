# Simple walpaper util

Downloads an image from the internet (into `~/Pictures/wallpapers`). And create a symlink at `"~/Pictures/wallpapers/wallpaper.png`

## Setup

**From inside this folder**
```sh
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

mkdir -p ~/.config/systemd/user/
eval "echo \"$(<wallpaper.service.template)\"" > ~/.config/systemd/user/wallpaper.service
systemctl enable wallpaper.service
```
