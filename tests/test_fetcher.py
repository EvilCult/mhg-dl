from fetcher import fetch_manga_info, MangaInfo

TEST_COMIC_ID = "30252"

def test_fetch_manga_info_basic():
    manga_info: MangaInfo = fetch_manga_info(TEST_COMIC_ID)

    # 检查对象类型
    assert isinstance(manga_info, MangaInfo)

    # 检查 title, cover, author 字段
    assert manga_info.title is not None
    assert isinstance(manga_info.title, str)
    assert manga_info.cover is None or isinstance(manga_info.cover, str)
    assert manga_info.author is None or isinstance(manga_info.author, str)

    # 检查 chapters 是字典，且嵌套字典正确:
    # {'单行本': {'第一卷': 'URL','第二卷': 'URL', ...}, '单话': {'第一话': 'URL'}, ...}
    assert isinstance(manga_info.chapters, dict)
    for group_name, chapters in manga_info.chapters.items():
        assert isinstance(group_name, str)
        assert isinstance(chapters, dict)
        for chapter_title, chapter_url in chapters.items():
            assert isinstance(chapter_title, str)
            assert isinstance(chapter_url, str)

def test_chapters_non_empty():
    # 检查 chapters 至少包含一组章节
    manga_info: MangaInfo = fetch_manga_info(TEST_COMIC_ID)
    assert len(manga_info.chapters) > 0
    for group_name, chapters in manga_info.chapters.items():
        assert len(chapters) > 0