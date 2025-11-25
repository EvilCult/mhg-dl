import os
import pytest
from unittest import mock
from mhg_dl.manga_downloader import download_chapter, download_image

# 临时目录 fixture
@pytest.fixture
def temp_dir(tmp_path):
    # tmp_path 是 pytest 自动提供的临时目录
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(orig_cwd)

# 模拟图片内容
@pytest.fixture
def fake_image_content():
    return b"fake image bytes"

# mock requests.get
@pytest.fixture
def mock_requests_get(fake_image_content):
    with mock.patch("mhg_dl.manga_downloader.requests.get") as mocked_get:
        mocked_resp = mock.Mock()
        mocked_resp.content = fake_image_content
        mocked_resp.raise_for_status = mock.Mock()
        mocked_get.return_value = mocked_resp
        yield mocked_get

def test_download_image_creates_file(temp_dir, mock_requests_get, fake_image_content):
    img_url = "http://example.com/image.jpg"
    img_path = temp_dir / "image.jpg"
    
    # 文件不存在时会下载
    download_image(img_url, str(img_path))
    assert img_path.exists()
    with open(img_path, "rb") as f:
        assert f.read() == fake_image_content
    
    # 文件存在时不会重新下载
    with mock.patch("builtins.print") as mock_print:
        download_image(img_url, str(img_path))
        mock_print.assert_any_call(f"Image already exists: {img_path}")

def test_download_chapter(temp_dir, mock_requests_get, fake_image_content):
    """测试 download_chapter 函数创建章节目录并下载图片"""
    chapter_name = "第1话"
    image_urls = [
        "http://example.com/1.jpg",
        "http://example.com/2.jpg",
        "http://example.com/3.png"
    ]
    save_dir = str(temp_dir / "单行本")
    
    # 调用 download_chapter
    download_chapter(chapter_name, image_urls, save_dir)
    
    # 检查章节目录是否创建
    chapter_dir = temp_dir / "单行本" / "第1话"
    assert chapter_dir.exists()
    
    # 检查图片文件是否下载
    assert (chapter_dir / "001.jpg").exists()
    assert (chapter_dir / "002.jpg").exists()
    assert (chapter_dir / "003.png").exists()
    
    # 验证文件内容
    for i in range(1, 4):
        if i == 3:
            img_file = chapter_dir / f"{i:03d}.png"
        else:
            img_file = chapter_dir / f"{i:03d}.jpg"
        with open(img_file, "rb") as f:
            assert f.read() == fake_image_content