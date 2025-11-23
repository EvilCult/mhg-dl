import os
import pytest
from unittest import mock
from mhg_dl.downloader import manga_download, download_image
from mhg_dl.models import MangaInfo

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
    with mock.patch("mhg_dl.downloader.requests.get") as mocked_get:
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

def test_manga_download_creates_dirs_and_files(temp_dir, mock_requests_get, fake_image_content):
    manga = MangaInfo(
        cid="123",
        title="Test Manga",
        cover="http://example.com/cover.jpg",
        author="Author Name",
        chapters={
            "单行本": {
                "第1话": [
                    "http://example.com/1.jpg",
                    "http://example.com/2.jpg"
                ]
            }
        }
    )

    manga_download(manga)

    # 检查目录
    manga_dir = temp_dir / "Test Manga - Author Name"
    assert manga_dir.exists()
    
    cover_path = manga_dir / "cover.jpg"
    assert cover_path.exists()

    chapter_dir = manga_dir / "单行本" / "第1话"
    assert chapter_dir.exists()
    
    # 检查图片文件
    for i in range(1, 3):
        img_file = chapter_dir / f"{i:03d}.jpg"
        assert img_file.exists()
        with open(img_file, "rb") as f:
            assert f.read() == fake_image_content