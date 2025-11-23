from mhg_dl.models import MangaInfo
from mhg_dl.fetcher import manga_fetch, chapter_fetch
from mhg_dl.downloader import manga_download

def download_command(args) -> None:
    fetch_filters: tuple[str, str] = (args.type, args.skip)
    manga: MangaInfo = manga_fetch(str(args.cid), fetch_filters)
    if manga.title == "":
        print("Comic not found")
        return

    manga = chapter_fetch(manga)
    # manga_download(manga)

def search_command(args) -> None:
    pass
