import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
# import time
# import random
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

    title, cover, author = fetch_base_info(soup)
    
    chapter_groups = fetch_chapter_list(soup)
    chapter_groups = select_chapter(chapter_groups, typ, skip)

    return MangaInfo(
        cid      = cid,
        title    = title,
        cover    = cover,
        author   = author,
        chapters =  chapter_groups
    )

def fetch_base_info(soup) -> tuple[str|None, str|None, str|None]:
    title = soup.select_one("h1").get_text(strip=True)

    cover_tag = soup.select_one(".book-cover > p > img")
    cover = "https:" + cover_tag["src"] if cover_tag else None

    author_tag = soup.select_one("ul.detail-list.cf > li:nth-child(2) > span:nth-child(2) > a")
    author = author_tag.get_text(strip=True) if author_tag else None

    return title, cover, author

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
    dl_chapters: dict[str, str] = chapters

    if typ != "all":
        dl_chapters = chapters[typ]

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
    for typ, chapters in manga.chapters.items():
        print(f"Analyzing: {typ}")
        for chapter_name, chapter_id in chapters.items():
            chapter_url: str = CHAPTER_URL.format(comic_id=manga.cid, chapter_id=chapter_id)
            
            # Random sleep 防止封禁
            # seconds = random.uniform(0, 2) 
            # time.sleep(seconds)

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
    # 不知道为什么要重复第一个字母,先hot fix一下
    def hot_fix_path(path: str) -> str:
        parts = path.split('/')
        parts[2] = f"{parts[2][0]}/{parts[2]}"
        return '/'.join(parts)
    
    dl_list: list[str] = []
    if "sl" not in chapter_data or "files" not in chapter_data:
        return dl_list
    
    for file_name in chapter_data["files"]:
        path: str = hot_fix_path(chapter_data["path"])
        image_url = IMAGE_URL.format(path=quote(path), file_name=file_name, e0=chapter_data["sl"]["e0"], e1=chapter_data["sl"]["e1"])
        dl_list.append(image_url)

    return dl_list
