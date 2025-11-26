import requests
from bs4 import BeautifulSoup
from mhg_dl.config import FAKE_HEADERS, SEARCH_URL
from mhg_dl.models import MangaInfo
from mhg_dl.manga_fetcher import manga_fetch
from mhg_dl.logger import log

def search_manga(query: str) -> list[MangaInfo]:
    results: list[MangaInfo] = []
    page: int = 1
    while page < 4:
        search_url = SEARCH_URL.format(query=query, page_suffix="" if page == 1 else f"_p{page}")

        try:
            response = requests.get(search_url, headers=FAKE_HEADERS)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results.extend(fmt_manga_info(soup))

            if not has_next_page(soup, page):
                break

            page += 1

        except Exception as e:
            log.error(f"Error searching for manga: {e}")
            break

    return results

def fmt_manga_info(soup: BeautifulSoup) -> MangaInfo:
    results: list[MangaInfo] = []

    for item in soup.select(".book-result > ul > li"):
        manga: MangaInfo = MangaInfo(
            cid   = item.select_one(".book-detail > dl > dt > a")["href"].split("/")[2],
            title = item.select_one(".book-detail > dl > dt > a").text.strip(),
            cover = "https:" + item.select_one(".book-cover > a > img")["src"],
            author= item.select_one(".book-detail > dl > dd:nth-child(4)").text.strip().split("：")[1],
            year  = item.select_one(".book-detail > dl > dd:nth-child(3) > span > a").text.strip(),
            stat  = item.select_one(".book-detail > dl > dd:nth-child(2) > span > span").text.strip(),
        ) 
        results.append(manga)
    
    return results

def has_next_page(soup: BeautifulSoup, current_page: int) -> bool:
    pager = soup.find("div", class_="pager", id="AspNetPagerResult")
    if not pager:
        return False

    next_page = pager.find("a", class_="prev")
    if next_page.text.strip() == "下一页":
        return True
    
    return False

def show_manga_details(cid: str) -> MangaInfo:
    manga: MangaInfo = manga_fetch(cid)

    return manga

