import argparse
from mhg_dl.main import download_command, search_command, info_command

def main() -> None:
    parser = argparse.ArgumentParser(description="mhg-dl, a simple comic download tool for manhuagui.com")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    parser_search = subparsers.add_parser("search", help="Search comic by keyword")
    parser_search.add_argument("query", type=str, help="Search keyword")
    parser_search.set_defaults(func=search_command)

    # info
    parser_info = subparsers.add_parser("info", help="Get comic information by comic id")
    parser_info.add_argument("cid", type=int, help="comic id")
    parser_info.set_defaults(func=info_command)

    # download
    parser_get = subparsers.add_parser("get", help="Download comic")
    parser_get.add_argument("cid", type=int, help="comic id")
    parser_get.add_argument("-o", "--output", type=str, default="./", help="Output directory")
    parser_get.add_argument("-t", "--type", type=str, default="all", help="Type of content to download")
    parser_get.add_argument("-s", "--skip", type=str, default=None, help="Skip previous content, start from specified chapter")
    parser_get.add_argument("-p", "--pick", type=str, default=None, help="Pick a specific chapter to download")
    parser_get.add_argument("-v", "--verbose", action="store_true", help="Verbose output (disable single-line progress)")
    parser_get.set_defaults(func=download_command)

    args = parser.parse_args()
    
    from mhg_dl.logger import log
    log.set_verbose(getattr(args, "verbose", False))

    args.func(args)

if __name__ == "__main__":
    main()