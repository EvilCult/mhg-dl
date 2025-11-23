from mhg_dl.models import MangaInfo
from mhg_dl.manga_fetcher import manga_fetch, chapter_fetch
from mhg_dl.manga_downloader import manga_download
from mhg_dl.manga_seacher import search_manga

def download_command(args) -> None:
    fetch_filters: tuple[str, str] = (args.type, args.skip)
    manga: MangaInfo = manga_fetch(str(args.cid), fetch_filters)
    if manga.title == "":
        print("Comic not found")
        return

    manga = chapter_fetch(manga)
    manga_download(manga)

    print(f"Download completed: {manga.title}")

def search_command(args) -> None:
    results = search_manga(args.query)
    if not results:
        print("No results found.")
        return

    for manga in results:
        print(f"[{manga.cid}] | {manga.title} ({manga.year}) - {manga.stat} - {manga.author}")

def info_command(args) -> None:
    pass