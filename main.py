import os
import shutil
import sys

import requests

HEADERS = {"User-Agent": "wallpaper-dl/1.0"}


def find_image(url="https://www.reddit.com/r/wallpapers/.json"):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    for post in r.json()["data"]["children"]:
        url = post["data"].get("url", "")
        if url.startswith("https://i.redd.it/"):
            return url, post["data"].get("title", "")
    return None, None


def download_image(url, title, dest):
    if not url:
        print("No image found")
        return False

    ext = os.path.splitext(url)[1]
    name = (title or os.path.basename(url)).replace("/", "_") + ext
    filename = os.path.join(dest, name)
    if os.path.exists(filename):
        print(f"Image already exists: {filename}")
        return False

    r = requests.get(url, headers=HEADERS, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        print(filename)
        return True
    else:
        print(f"Failed to download image: {url}")
        return False


if __name__ == "__main__":
    download_dir = sys.argv[1]
    download_folder = os.path.expanduser(download_dir)
    os.makedirs(download_folder, exist_ok=True)

    url, title = find_image()
    ret = download_image(url, title, download_folder)
    sys.exit(0 if ret else 1)
