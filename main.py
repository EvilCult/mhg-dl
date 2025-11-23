import argparse
from models import MangaInfo
from fetcher import manga_fetch, chapter_fetch
from downloader import manga_download

def download_command(args) -> None:
    fetch_filters: tuple[str, str] = (args.type, args.skip)
    manga: MangaInfo = manga_fetch(str(args.cid), fetch_filters)
    if manga.title == "":
        print("Comic not found")
        return

    manga = chapter_fetch(manga)
    manga_download(manga)

def search_command(args) -> None:
    pass

def main() -> None:
    parser = argparse.ArgumentParser(description="mhg-dl, a simple comic download tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    parser_search = subparsers.add_parser("search", help="Search comic by keyword")
    parser_search.add_argument("query", type=str, help="Search keyword")
    parser_search.set_defaults(func=search_command)

    # download
    parser_get = subparsers.add_parser("get", help="Download comic")
    parser_get.add_argument("cid", type=int, help="comic id")
    parser_get.add_argument("-t", "--type", type=str, default="all", help="Type of content to download")
    parser_get.add_argument("-s", "--skip", type=str, default=None, help="Skip previous content, start from specified chapter")
    parser_get.set_defaults(func=download_command)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()