import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import random
from mhg_dl.unpacker import unpack
from mhg_dl.models import MangaInfo
from mhg_dl.config import FAKE_HEADERS, MANGA_URL, CHAPTER_URL, IMAGE_URL

def manga_fetch(cid: str, fetch_filters: tuple[str, str]) -> MangaInfo:
    url = MANGA_URL.format(comic_id=cid)
    typ, skip = tuple(fetch_filters)

    try:
        resp = requests.get(url, headers=FAKE_HEADERS)
        resp.raise_for_status()
    except Exception :
        print("The comic id is wrong or the comic does not exist.")
        return MangaInfo(cid=cid, title="")

    soup = BeautifulSoup(resp.text, "html.parser")

    manga: MangaInfo = fetch_base_info(cid, soup)
    
    chapter_groups = fetch_chapter_list(soup)
    chapter_groups = select_chapter(chapter_groups, typ, skip)
    manga.chapters = chapter_groups

    return manga

def fetch_base_info(cid: str, soup: BeautifulSoup) -> MangaInfo:
    title_elem = soup.select_one(".book-title > h1")
    cover_elem = soup.select_one(".book-cover > p > img")
    author_elem = soup.select_one(".book-detail > ul.detail-list > li:nth-child(2) > span:nth-child(2) > a")
    year_elem = soup.select_one(".book-detail > ul.detail-list > li:nth-child(1) > span:nth-child(1) > a")
    stat_elem = soup.select_one(".book-detail > ul.detail-list > li:nth-child(4) > span")

    manga = MangaInfo(
        cid    = cid,
        title  = title_elem.text.strip() if title_elem else None,
        cover  = "https:" + cover_elem["src"] if cover_elem else None,
        author = author_elem.text.strip() if author_elem else None,
        year   = year_elem.text.strip() if year_elem else None,
        stat   = stat_elem.text.strip().split("：")[1] if stat_elem and "：" in stat_elem.text else None,
    )
    return manga

def fetch_chapter_list(soup) -> dict[str, dict[str, str]]:
    chapter_groups: dict[str, dict[str, str]] = {}

    type_list = [span.get_text(strip=True) for span in soup.select("h4 > span")]

    list_groups = soup.select("div.chapter-list")
    for idx, group in enumerate(list_groups):
        chapter_parts = group.select("ul")
        content_list: dict[str, str] = {}
        for part in chapter_parts:
            tmp: dict[str, str] = {}
            for li in part.select("li"):
                chapter_title = li.find("span").find(string=True, recursive=False)
                chapter_url = li.find("a")["href"]
                tmp[chapter_title] = chapter_url.split("/")[3].replace(".html", "")
            content_list.update(dict(reversed(list(tmp.items()))))
        chapter_groups[type_list[idx]] = content_list

    return chapter_groups

def select_chapter(chapters: dict[str, dict[str, str]], typ: str, skip: str) -> dict[str, dict[str, str]]:
    if typ == "all":
        return chapters

    dl_chapters: dict[str, str] = chapters[typ]
    if skip is not None:
        skiping: bool = True
        tmp: dict[str, str] = {}
        for key, value in dl_chapters.items():
            if key == skip:
                skiping = False
            if not skiping:
                tmp[key] = value
        dl_chapters = tmp

    return  {typ: dl_chapters}

def chapter_fetch(manga: MangaInfo) -> MangaInfo:
    print("(*≧▽≦) Let's go!\n")
    for typ, chapters in manga.chapters.items():
        print(f"Analyzing: {typ}")
        for chapter_name, chapter_id in chapters.items():
            chapter_url: str = CHAPTER_URL.format(comic_id=manga.cid, chapter_id=chapter_id)
            
            # Random sleep
            seconds = random.uniform(0, 2) 
            time.sleep(seconds)

            print(f"Analyzing: {chapter_name} ({chapter_url})")
            images_data = analyze_chapter(chapter_url)
            chapters[chapter_name] = make_img_list(images_data)
    return manga

def analyze_chapter(chapter_url: str) -> dict[str, any]:
    chapter_data: dict[str, any] = {}
    try:
        resp = requests.get(chapter_url, headers=FAKE_HEADERS)
        resp.raise_for_status()
    except Exception:
        print(f"Unable to access: {chapter_url}")
        return chapter_data

    soup = BeautifulSoup(resp.text, "html.parser")
    script_tags = soup.find_all("script")
    for x in script_tags:
        script_text = x.get_text()
        if r'["\x65\x76\x61\x6c"]' in script_text:
            chapter_data = unpack(script_text)
    return chapter_data

def make_img_list(chapter_data: dict[str, any]) -> list[str]:
    dl_list: list[str] = []
    if "sl" not in chapter_data or "files" not in chapter_data:
        return dl_list
    
    for file_name in chapter_data["files"]:
        path: str = chapter_data["path"]
        image_url = IMAGE_URL.format(path=quote(path), file_name=file_name, e0=chapter_data["sl"]["e"], e1=chapter_data["sl"]["m"])
        dl_list.append(image_url)

    return dl_list
