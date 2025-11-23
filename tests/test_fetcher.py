import requests
from bs4 import BeautifulSoup

from mhg_dl.manga_fetcher import (
    manga_fetch,
    MangaInfo,
    fetch_base_info,
    fetch_chapter_list,
    analyze_chapter,
    make_img_list,
)


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")


def test_fetch_base_info_and_chapter_list():
    # Build a minimal HTML page matching selectors used in fetcher
    html = '''
    <html>
      <body>
        <h1>测试漫</h1>
        <div class="book-cover"><p><img src="//cover.example/img.jpg"/></p></div>
        <ul class="detail-list cf">
          <li></li>
          <li><span></span><span><a href="/author/1">作者名</a></span></li>
        </ul>
        <h4><span>单话</span></h4>
        <div class="chapter-list">
          <ul>
            <li><span>第一话</span><a href="/comic/123/1001.html">link</a></li>
            <li><span>第二话</span><a href="/comic/123/1002.html">link</a></li>
          </ul>
        </div>
      </body>
    </html>
    '''

    soup = BeautifulSoup(html, "html.parser")
    title, cover, author = fetch_base_info(soup)
    assert title == "测试漫"
    assert cover == "https://cover.example/img.jpg"
    assert author == "作者名"

    chapter_groups = fetch_chapter_list(soup)
    assert isinstance(chapter_groups, dict)
    assert "单话" in chapter_groups
    chapters = chapter_groups["单话"]
    # reversed order in implementation, so expect keys
    assert list(chapters.keys()) == ["第二话", "第一话"]


def test_manga_fetch_handles_http_error(monkeypatch):
    # Simulate network error
    def fake_get(*args, **kwargs):
        raise requests.RequestException("network")

    monkeypatch.setattr("requests.get", fake_get)
    info = manga_fetch("no-such-cid", fetch_filters=("all", None))
    assert isinstance(info, MangaInfo)
    assert info.title == ""


def test_analyze_chapter_uses_unpack(monkeypatch):
    # page with a script containing the special eval pattern
    script_html = '<script>some();["\\x65\\x76\\x61\\x6c"]</script>'
    page_html = f"<html><body>{script_html}</body></html>"

    def fake_get(url, headers=None):
        return FakeResponse(page_html)

    monkeypatch.setattr("requests.get", fake_get)

    # patch unpack to return a dict we control
    monkeypatch.setattr("mhg_dl.manga_fetcher.unpack", lambda s: {"files": ["a.jpg"], "sl": {"e0": 1, "e1": 2}, "path": "/p/"})

    result = analyze_chapter("http://example/chapter.html")
    assert isinstance(result, dict)
    assert result["files"] == ["a.jpg"]


def test_make_img_list_builds_urls():
    chapter_data = {
        "files": ["1.jpg", "2.jpg"],
        "path": "/path/to/",
        "sl": {"e0": 111, "e1": 222},
    }
    result = make_img_list(chapter_data)
    assert len(result) == 2
    for file_name, url in zip(chapter_data["files"], result):
        assert file_name in url
        assert str(chapter_data["sl"]["e0"]) in url