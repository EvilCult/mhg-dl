from dataclasses import dataclass, field
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

API_URL = "https://www.manhuagui.com/comic/{comic_id}/"

@dataclass
class MangaInfo:
    title: str
    cover: str | None = None
    author: str | None = None
    chapters: Dict[str, Dict[str, str]] = field(default_factory=dict)

def fetch_manga_info(cid: str) -> MangaInfo:
    url = API_URL.format(comic_id=cid)

    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title, cover, author = fetch_base_info(soup)
    
    chapter_groups = fetch_chapter_list(soup)

    return MangaInfo(
        title=title,
        cover=cover,
        author=author,
        chapters=chapter_groups
    )

def fetch_base_info(soup) -> tuple[str|None, str|None, str|None]:
    title = soup.select_one("h1").get_text(strip=True)

    cover_tag = soup.select_one(".book-cover > p > img")
    cover = "https:" + cover_tag["src"] if cover_tag else None

    author_tag = soup.select_one("ul.detail-list.cf > li:nth-child(2) > span:nth-child(2) > a")
    author = author_tag.get_text(strip=True) if author_tag else None

    return title, cover, author

def fetch_chapter_list(soup) -> Dict[str, List[str]]:
    chapter_groups: Dict[str, Dict[str, str]] = {}

    type_list = [span.get_text(strip=True) for span in soup.select("h4 > span")]

    list_groups = soup.select("div#chapter-list-1")
    for idx, group in enumerate(list_groups):
        chapter_parts = group.select("ul")
        content_list: Dict[str, str ] = {}
        for part in chapter_parts:
            tmp: Dict[str, str ] = {}
            for li in part.select("li"):
                chapter_title = li.find("span").find(string=True, recursive=False)
                chapter_url = li.find("a")["href"]
                tmp[chapter_title] = chapter_url
            content_list.update(dict(reversed(list(tmp.items()))))
        chapter_groups[type_list[idx]] = content_list

    return chapter_groups
