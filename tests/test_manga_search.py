# test_manga_search.py
import pytest
from mhg_dl.manga_seacher import search_manga
from mhg_dl.models import MangaInfo

def test_search_manga_basic():
    query = "测试漫画"  # 可换成实际存在的关键字
    results = search_manga(query)

    # 确保返回是列表
    assert isinstance(results, list), "结果应该是一个列表"

    if results:
        manga = results[0]
        # 确保返回对象是 MangaInfo
        assert isinstance(manga, MangaInfo), "返回的对象应为 MangaInfo"
        # 核心字段非空
        assert manga.cid, "cid 不应为空"
        assert manga.title, "title 不应为空"
        # 可选字段允许为空
        assert manga.cover is None or isinstance(manga.cover, str)
        assert manga.author is None or isinstance(manga.author, str)
        assert manga.year is None or isinstance(manga.year, str)
        assert manga.stat is None or isinstance(manga.stat, str)

def test_search_manga_no_results():
    # 使用一个不可能的关键字确保返回空列表
    query = "asdhaskdhakjshdkajshd"  
    results = search_manga(query)
    assert results == [], "无匹配时应返回空列表"

if __name__ == "__main__":
    pytest.main()