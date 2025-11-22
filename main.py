import argparse
import fetcher

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

def main() -> None:
    parser = argparse.ArgumentParser(description="mhg-dl, 一个简单的漫画下载工具")

    parser.add_argument("--cid", "-c", type=int, default=1, help="漫画cid, 如 https://www.manhuagui.com/comic/**cid**/")
    parser.add_argument("--type", "-t", type=str, default="all", help="下载内容的类型, 如: 单行本, 单话等")
    parser.add_argument("--skip", "-s", type=str, default=None, help="跳过之前内容, 从指定章节开始下载, 章节名称需与目录一致")

    args = parser.parse_args()

    data = fetcher.fetch_manga_info(str(args.cid))

    if data.title == "":
        return None

    data.chapters = select_chapter(data.chapters, args.type, args.skip)

    print(data)


if __name__ == "__main__":
    main()
