import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from dataclasses import dataclass, field
import time
import random
from unpacker import unpack

MANGA_URL = "https://www.manhuagui.com/comic/{comic_id}/"
CHAPTER_URL = "https://www.manhuagui.com/comic/{comic_id}/{chapter_id}.html"
IMAGE_URL = "https://us2.hamreus.com{path}{file_name}?e={e0}&m={e1}"

@dataclass
class MangaInfo:
    cid: str
    title: str
    cover: str | None = None
    author: str | None = None
    chapters: dict[str, dict[str, str | list[str]]] = field(default_factory=dict)

def manga_fetch(cid: str) -> MangaInfo:
    url = MANGA_URL.format(comic_id=cid)

    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception :
        print("漫画id错误 或 漫画不存在.")
        return MangaInfo(cid=cid, title="", cover=None, author=None, chapters={})

    soup = BeautifulSoup(resp.text, "html.parser")

    title, cover, author = fetch_base_info(soup)
    
    chapter_groups = fetch_chapter_list(soup)

    return MangaInfo(
        cid = cid,
        title = title,
        cover = cover,
        author = author,
        chapters = chapter_groups
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

def chapter_fetch(manga: MangaInfo) -> MangaInfo:
    for typ, chapters in manga.chapters.items():
        print(f"下载类型: {typ}")
        for chapter_name, chapter_id in chapters.items():
            chapter_url: str = CHAPTER_URL.format(comic_id=manga.cid, chapter_id=chapter_id)
            
            seconds = random.uniform(1, 5) 
            print(f"随机睡眠{seconds:.2f}秒以防封禁...")
            time.sleep(seconds)

            print(f"开始分析: {chapter_name} ({chapter_url})")
            images_data = analyze_chapter(chapter_url)
            chapters[chapter_name] = make_img_list(images_data)
    return manga

def analyze_chapter(chapter_url: str) -> dict[str, any]:
    chapter_data: dict[str, any] = {}
    try:
        resp = requests.get(chapter_url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception:
        print(f"无法访问页面: {chapter_url}")
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
        image_url = IMAGE_URL.format(path=quote(chapter_data["path"]), file_name=file_name, e0=chapter_data["sl"]["e0"], e1=chapter_data["sl"]["e1"])
        dl_list.append(image_url)

    return dl_list
