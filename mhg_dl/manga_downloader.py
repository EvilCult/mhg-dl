import os
import requests
# import time
# import random
from mhg_dl.models import MangaInfo
from mhg_dl.config import FAKE_HEADERS

def manga_download(manga: MangaInfo) -> None:
    title: str = manga.title
    authour: str | None = manga.author
    cover: str | None = manga.cover

    manga_dir_name = f"{title} - {authour}" if authour else title
    download_dir = os.path.join(os.getcwd(), manga_dir_name)
    os.makedirs(download_dir, exist_ok=True)

    if cover:
        cover_path = os.path.join(download_dir, "cover.jpg")
        download_image(cover, cover_path)

    for typ, chapters in manga.chapters.items():
        print(f"Downloading: {typ}")
        type_dir = os.path.join(download_dir, typ)
        os.makedirs(type_dir, exist_ok=True)

        for chapter_name, image_urls in chapters.items():
            print(f"Downloading: {chapter_name}")
            chapter_dir = os.path.join(type_dir, chapter_name)
            os.makedirs(chapter_dir, exist_ok=True)

            for idx, img_url in enumerate(image_urls):
                img_ext = os.path.splitext(img_url)[1].split("?")[0]
                img_name = f"{idx + 1:03d}{img_ext}"
                img_path = os.path.join(chapter_dir, img_name)
                download_image(img_url, img_path)

def download_image(url: str, path: str) -> None:
    if os.path.exists(path):
        print(f"Image already exists: {path}")
        return
    try:
        print(f"Downloading: {url}")

        # Random sleep 防止封禁
        # seconds = random.uniform(0, 2) 
        # time.sleep(seconds)

        resp = requests.get(url, headers=FAKE_HEADERS)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")
