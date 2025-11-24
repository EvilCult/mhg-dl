from mhg_dl.models import MangaInfo
from mhg_dl.manga_fetcher import manga_fetch, chapter_fetch
from mhg_dl.manga_downloader import manga_download
from mhg_dl.manga_seacher import search_manga, show_manga_details

def download_command(args) -> None:
    fetch_filters: tuple[str, str] = (args.type, args.skip)
    manga: MangaInfo = manga_fetch(str(args.cid), fetch_filters)
    if manga.title == "":
        print("Comic not found")
        return

    manga = chapter_fetch(manga)
    manga_download(manga)

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