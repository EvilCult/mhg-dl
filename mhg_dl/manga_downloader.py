import os
import requests
import time
import random

from mhg_dl.config import FAKE_HEADERS

def download_chapter(chapter_name: str, image_urls: list[str], save_dir: str) -> None:
    print(f"\n٩(๑>◡<๑)۶ Downloading: {chapter_name}")
    chapter_dir = os.path.join(save_dir, chapter_name)
    os.makedirs(chapter_dir, exist_ok=True)

    for idx, img_url in enumerate(image_urls):
        img_ext  = os.path.splitext(img_url)[1].split("?")[0]
        img_name = f"{idx + 1:03d}{img_ext}"
        img_path = os.path.join(chapter_dir, img_name)
        download_image(img_url, img_path)

def download_image(url: str, path: str) -> None:
    if os.path.exists(path):
        print(f"Image already exists: {path}")
        return
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            if attempt == 1:
                print(f"✓ Downloading: {url}")
            else:
                print(f"↻ Retry {attempt - 1}: {url}")

            # Random sleep 防止封禁
            seconds = random.uniform(0, 2)
            time.sleep(seconds)

            resp = requests.get(url, headers=FAKE_HEADERS, timeout=10)
            resp.raise_for_status()

            with open(path, "wb") as f:
                f.write(resp.content)

            return

        except Exception as e:
            if attempt < max_retries:
                print(f"↩︎ Cooling down before retrying... ({e})")
                time.sleep(5)
            else:
                print(f"✗ Failed after {max_retries} tries: {url} ({e})")
