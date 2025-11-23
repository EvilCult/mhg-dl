import requests
from bs4 import BeautifulSoup
from mhg_dl.config import FAKE_HEADERS, SEARCH_URL
from mhg_dl.models import MangaInfo

def search_manga(query: str) -> list[MangaInfo]:
    search_url = SEARCH_URL.format(query=query)
    try:
        response = requests.get(search_url, headers=FAKE_HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
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

    except Exception as e:
        print(f"Error searching for manga: {e}")
        return []