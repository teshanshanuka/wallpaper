import requests
from bs4 import BeautifulSoup
import os
import sys
import re
import shutil


def load_page(url="https://www.reddit.com/r/wallpapers/"):
    r = requests.get(url)
    return r.text


def find_image(html):
    """
    find all <img> matching src="https://i.redd.it/*.png"
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("img", src=re.compile(r"^https://i.redd.it/.*\.png$"))


def get_image_name(img_elem):
    if name := img_elem.get("alt", ""):
        name = os.path.basename(name).replace("wallpapers - ", "")
    else:
        name = os.path.basename(img_elem["src"])
    return name + ".png"


def download_image(img_elem, dest: str):
    url = img_elem["src"]
    filename = os.path.join(dest, get_image_name(img_elem))
    if os.path.exists(filename):
        print(f"Image already exists: {filename}")
        return False

    r = requests.get(url, stream=True)
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
    html = load_page()

    download_folder = os.path.expanduser(download_dir)
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)

    image = find_image(html)
    ret = download_image(image, download_folder)

    sys.exit(0 if ret else 1)
