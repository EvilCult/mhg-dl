import os
import time
import random
from mhg_dl.models import MangaInfo
from mhg_dl.config import CHAPTER_URL
from mhg_dl.manga_fetcher import manga_fetch, filter_chapter, get_chapter_image_urls
from mhg_dl.manga_downloader import download_chapter, download_image
from mhg_dl.manga_seacher import search_manga, show_manga_details

def download_command(args) -> None:
    manga: MangaInfo = manga_fetch(str(args.cid))
    if manga.title == "":
        print("Comic not found")
        return
    
    manga.chapters = filter_chapter(manga.chapters, args.type, args.skip, args.pick)

    # Prepare download directory
    title = manga.title
    author = manga.author
    manga_dir_name = f"{title} - {author}" if author else title
    download_dir = os.path.join(os.getcwd(), manga_dir_name)
    os.makedirs(download_dir, exist_ok=True)

    # Download cover
    if manga.cover:
        cover_path = os.path.join(download_dir, "cover.jpg")
        download_image(manga.cover, cover_path)

    print("(*≧▽≦) Let's go!\n")
    for typ, chapters in manga.chapters.items():
        print(f"\n(ง •̀_•́)ง Starting...: {typ}")
        type_dir = os.path.join(download_dir, typ)
        os.makedirs(type_dir, exist_ok=True)

        for chapter_name, chapter_id in chapters.items():
            chapter_url = CHAPTER_URL.format(comic_id=manga.cid, chapter_id=chapter_id)
            
            # Random sleep
            seconds = random.uniform(0, 2) 
            time.sleep(seconds)

            image_urls = get_chapter_image_urls(manga.cid, chapter_url)
            download_chapter(chapter_name, image_urls, type_dir)

    print(f"\n(*´Д｀)=3 Done! -->  {manga.title}")

def search_command(args) -> None:
    results = search_manga(args.query)
    if not results:
        print("No results found.")
        return

    for manga in results:
        print(f"[{manga.cid}] | {manga.title} ({manga.year}) - {manga.stat} - {manga.author}")

def info_command(args) -> None:
    manga: MangaInfo = show_manga_details(args.cid)

    if manga.title is None:
        print("Comic not found.")
        return
    print(f"Comic id : {manga.cid}")
    print(f"Title    : {manga.title}")
    print(f"Author   : {manga.author}")
    print(f"Year     : {manga.year}")
    print(f"Status   : {manga.stat}")
    print(f"Cover    : {manga.cover}")
    print("Chapters: (latest 15 chapters)")
    for chap_type, chapters in manga.chapters.items():
        print(f"- {chap_type} : [{len(chapters)}]")
        for chap_title in list(reversed(chapters.keys()))[:15]:
            print(f"  -- {chap_title}")