import os
import pytest
from unittest import mock
from argparse import Namespace

from mhg_dl.main import download_command, search_command, info_command
from mhg_dl.models import MangaInfo


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_dir(tmp_path):
    """临时目录 fixture，自动切换工作目录"""
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(orig_cwd)


@pytest.fixture
def mock_manga_info():
    """创建一个模拟的漫画信息对象"""
    return MangaInfo(
        cid="12345",
        title="测试漫画",
        author="测试作者",
        cover="http://example.com/cover.jpg",
        year="2024",
        stat="连载中",
        chapters={
            "单行本": {
                "第1话": "1001",
                "第2话": "1002",
            },
            "番外篇": {
                "番外1": "2001",
            }
        }
    )


@pytest.fixture
def mock_manga_info_no_author():
    """创建一个没有作者的漫画信息"""
    return MangaInfo(
        cid="12345",
        title="测试漫画",
        author=None,
        cover=None,
        chapters={
            "单行本": {
                "第1话": "1001",
            }
        }
    )


@pytest.fixture
def download_args():
    """下载命令的参数对象"""
    return Namespace(
        cid="12345",
        type="all",
        skip=None,
        pick=None
    )


@pytest.fixture
def search_args():
    """搜索命令的参数对象"""
    return Namespace(query="测试")


@pytest.fixture
def info_args():
    """信息命令的参数对象"""
    return Namespace(cid="12345")


# ============================================================================
# Tests for download_command
# ============================================================================

def test_download_command_success(temp_dir, download_args, mock_manga_info, monkeypatch):
    """测试完整的下载流程（正常情况）"""
    # Mock 所有外部依赖
    mock_manga_fetch = mock.Mock(return_value=mock_manga_info)
    mock_filter_chapter = mock.Mock(return_value=mock_manga_info.chapters)
    mock_download_image = mock.Mock()
    mock_get_chapter_image_urls = mock.Mock(return_value=[
        "http://example.com/1.jpg",
        "http://example.com/2.jpg"
    ])
    mock_download_chapter = mock.Mock()
    mock_sleep = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.manga_fetch", mock_manga_fetch)
    monkeypatch.setattr("mhg_dl.main.filter_chapter", mock_filter_chapter)
    monkeypatch.setattr("mhg_dl.main.download_image", mock_download_image)
    monkeypatch.setattr("mhg_dl.main.get_chapter_image_urls", mock_get_chapter_image_urls)
    monkeypatch.setattr("mhg_dl.main.download_chapter", mock_download_chapter)
    monkeypatch.setattr("mhg_dl.main.time.sleep", mock_sleep)
    
    # 执行下载命令
    download_command(download_args)
    
    # 验证 manga_fetch 被调用
    mock_manga_fetch.assert_called_once_with("12345")
    
    # 验证 filter_chapter 被调用
    mock_filter_chapter.assert_called_once_with(
        mock_manga_info.chapters,
        "all",
        None,
        None
    )
    
    # 验证目录结构创建正确
    expected_dir = temp_dir / "测试漫画 - 测试作者"
    assert expected_dir.exists()
    assert (expected_dir / "单行本").exists()
    assert (expected_dir / "番外篇").exists()
    
    # 验证封面下载被调用
    mock_download_image.assert_called_once()
    cover_call = mock_download_image.call_args
    assert cover_call[0][0] == "http://example.com/cover.jpg"
    assert "cover.jpg" in cover_call[0][1]
    
    # 验证章节图片URL获取被调用（3个章节）
    assert mock_get_chapter_image_urls.call_count == 3
    
    # 验证章节下载被调用（3个章节）
    assert mock_download_chapter.call_count == 3
    
    # 验证第一个章节的调用
    first_call = mock_download_chapter.call_args_list[0]
    assert first_call[0][0] == "第1话"  # chapter_name
    assert first_call[0][1] == ["http://example.com/1.jpg", "http://example.com/2.jpg"]  # image_urls
    
    # 验证 sleep 被调用（每个章节调用一次）
    assert mock_sleep.call_count == 3


def test_download_command_manga_not_found(download_args, monkeypatch):
    """测试漫画不存在时的处理"""
    # Mock manga_fetch 返回空标题
    empty_manga = MangaInfo(cid="12345", title="")
    mock_manga_fetch = mock.Mock(return_value=empty_manga)
    monkeypatch.setattr("mhg_dl.main.manga_fetch", mock_manga_fetch)
    
    # Mock print 以验证输出
    mock_print = mock.Mock()
    monkeypatch.setattr("builtins.print", mock_print)
    
    # 执行下载命令
    download_command(download_args)
    
    # 验证打印了错误信息
    mock_print.assert_called_with("Comic not found")
    
    # 验证 manga_fetch 被调用
    mock_manga_fetch.assert_called_once_with("12345")


def test_download_command_without_cover(temp_dir, download_args, mock_manga_info, monkeypatch):
    """测试没有封面时的处理"""
    # 修改 mock_manga_info，移除封面
    mock_manga_info.cover = None
    
    mock_manga_fetch = mock.Mock(return_value=mock_manga_info)
    mock_filter_chapter = mock.Mock(return_value=mock_manga_info.chapters)
    mock_download_image = mock.Mock()
    mock_get_chapter_image_urls = mock.Mock(return_value=["http://example.com/1.jpg"])
    mock_download_chapter = mock.Mock()
    mock_sleep = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.manga_fetch", mock_manga_fetch)
    monkeypatch.setattr("mhg_dl.main.filter_chapter", mock_filter_chapter)
    monkeypatch.setattr("mhg_dl.main.download_image", mock_download_image)
    monkeypatch.setattr("mhg_dl.main.get_chapter_image_urls", mock_get_chapter_image_urls)
    monkeypatch.setattr("mhg_dl.main.download_chapter", mock_download_chapter)
    monkeypatch.setattr("mhg_dl.main.time.sleep", mock_sleep)
    
    # 执行下载命令
    download_command(download_args)
    
    # 验证封面下载没有被调用
    mock_download_image.assert_not_called()
    
    # 验证章节下载正常进行
    assert mock_download_chapter.call_count == 3


def test_download_command_creates_correct_directory_structure(temp_dir, download_args, monkeypatch):
    """测试目录创建逻辑（有作者 vs 无作者）"""
    # 测试有作者的情况
    manga_with_author = MangaInfo(
        cid="12345",
        title="测试漫画",
        author="测试作者",
        chapters={"单行本": {"第1话": "1001"}}
    )
    
    mock_manga_fetch = mock.Mock(return_value=manga_with_author)
    mock_filter_chapter = mock.Mock(return_value=manga_with_author.chapters)
    mock_download_image = mock.Mock()
    mock_get_chapter_image_urls = mock.Mock(return_value=[])
    mock_download_chapter = mock.Mock()
    mock_sleep = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.manga_fetch", mock_manga_fetch)
    monkeypatch.setattr("mhg_dl.main.filter_chapter", mock_filter_chapter)
    monkeypatch.setattr("mhg_dl.main.download_image", mock_download_image)
    monkeypatch.setattr("mhg_dl.main.get_chapter_image_urls", mock_get_chapter_image_urls)
    monkeypatch.setattr("mhg_dl.main.download_chapter", mock_download_chapter)
    monkeypatch.setattr("mhg_dl.main.time.sleep", mock_sleep)
    
    download_command(download_args)
    
    # 验证目录名包含作者
    expected_dir = temp_dir / "测试漫画 - 测试作者"
    assert expected_dir.exists()
    
    # 清理
    import shutil
    shutil.rmtree(expected_dir)
    
    # 测试无作者的情况
    manga_without_author = MangaInfo(
        cid="12345",
        title="测试漫画",
        author=None,
        chapters={"单行本": {"第1话": "1001"}}
    )
    mock_manga_fetch.return_value = manga_without_author
    mock_filter_chapter.return_value = manga_without_author.chapters
    
    download_command(download_args)
    
    # 验证目录名不包含作者
    expected_dir_no_author = temp_dir / "测试漫画"
    assert expected_dir_no_author.exists()


def test_download_command_respects_chapter_filter(temp_dir, monkeypatch):
    """测试章节过滤参数传递正确"""
    # 创建原始漫画信息（未过滤）
    original_chapters = {
        "单行本": {
            "第1话": "1001",
            "第2话": "1002",
        },
        "番外篇": {
            "番外1": "2001",
        }
    }
    
    original_manga_info = MangaInfo(
        cid="12345",
        title="测试漫画",
        author="测试作者",
        cover="http://example.com/cover.jpg",
        chapters=original_chapters.copy()  # 使用副本
    )
    
    # 创建带过滤的参数
    filtered_args = Namespace(
        cid="12345",
        type="单行本",
        skip="第1话",
        pick=None
    )
    
    # 模拟 filter_chapter 返回过滤后的结果
    filtered_chapters = {"单行本": {"第2话": "1002"}}
    
    mock_manga_fetch = mock.Mock(return_value=original_manga_info)
    mock_filter_chapter = mock.Mock(return_value=filtered_chapters)
    mock_download_image = mock.Mock()
    mock_get_chapter_image_urls = mock.Mock(return_value=["http://example.com/1.jpg"])
    mock_download_chapter = mock.Mock()
    mock_sleep = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.manga_fetch", mock_manga_fetch)
    monkeypatch.setattr("mhg_dl.main.filter_chapter", mock_filter_chapter)
    monkeypatch.setattr("mhg_dl.main.download_image", mock_download_image)
    monkeypatch.setattr("mhg_dl.main.get_chapter_image_urls", mock_get_chapter_image_urls)
    monkeypatch.setattr("mhg_dl.main.download_chapter", mock_download_chapter)
    monkeypatch.setattr("mhg_dl.main.time.sleep", mock_sleep)
    
    download_command(filtered_args)
    
    # 验证 filter_chapter 被正确调用
    mock_filter_chapter.assert_called_once()
    call_args = mock_filter_chapter.call_args[0]
    
    # 验证传入的参数（比较字典内容）
    assert call_args[0] == original_chapters  # chapters 字典
    assert call_args[1] == "单行本"  # type
    assert call_args[2] == "第1话"  # skip
    assert call_args[3] is None  # pick
    
    # 验证只下载了1个章节（过滤后的）
    assert mock_download_chapter.call_count == 1
    
    # 验证下载的是正确的章节
    chapter_call_args = mock_download_chapter.call_args[0]
    assert chapter_call_args[0] == "第2话"


def test_download_command_with_empty_chapters(temp_dir, download_args, monkeypatch):
    """测试章节列表为空时的处理"""
    empty_manga = MangaInfo(
        cid="12345",
        title="测试漫画",
        author="测试作者",
        chapters={}
    )
    
    mock_manga_fetch = mock.Mock(return_value=empty_manga)
    mock_filter_chapter = mock.Mock(return_value={})
    mock_download_image = mock.Mock()
    mock_get_chapter_image_urls = mock.Mock()
    mock_download_chapter = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.manga_fetch", mock_manga_fetch)
    monkeypatch.setattr("mhg_dl.main.filter_chapter", mock_filter_chapter)
    monkeypatch.setattr("mhg_dl.main.download_image", mock_download_image)
    monkeypatch.setattr("mhg_dl.main.get_chapter_image_urls", mock_get_chapter_image_urls)
    monkeypatch.setattr("mhg_dl.main.download_chapter", mock_download_chapter)
    
    # 执行下载命令（不应该报错）
    download_command(download_args)
    
    # 验证目录被创建
    expected_dir = temp_dir / "测试漫画 - 测试作者"
    assert expected_dir.exists()
    
    # 验证章节下载没有被调用
    mock_get_chapter_image_urls.assert_not_called()
    mock_download_chapter.assert_not_called()


# ============================================================================
# Tests for search_command
# ============================================================================

def test_search_command_success(search_args, monkeypatch):
    """测试搜索命令（有结果）"""
    # Mock 搜索结果
    mock_results = [
        MangaInfo(cid="1", title="漫画1", year="2024", stat="连载中", author="作者1"),
        MangaInfo(cid="2", title="漫画2", year="2023", stat="完结", author="作者2"),
    ]
    
    mock_search_manga = mock.Mock(return_value=mock_results)
    mock_print = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.search_manga", mock_search_manga)
    monkeypatch.setattr("builtins.print", mock_print)
    
    search_command(search_args)
    
    # 验证 search_manga 被调用
    mock_search_manga.assert_called_once_with("测试")
    
    # 验证打印了结果（至少调用了2次，每个结果一次）
    assert mock_print.call_count == 2


def test_search_command_no_results(search_args, monkeypatch):
    """测试搜索命令（无结果）"""
    mock_search_manga = mock.Mock(return_value=[])
    mock_print = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.search_manga", mock_search_manga)
    monkeypatch.setattr("builtins.print", mock_print)
    
    search_command(search_args)
    
    # 验证打印了"无结果"信息
    mock_print.assert_called_once_with("No results found.")


# ============================================================================
# Tests for info_command
# ============================================================================

def test_info_command_success(info_args, monkeypatch):
    """测试信息命令（漫画存在）"""
    mock_manga = MangaInfo(
        cid="12345",
        title="测试漫画",
        author="测试作者",
        year="2024",
        stat="连载中",
        cover="http://example.com/cover.jpg",
        chapters={
            "单行本": {f"第{i}话": f"100{i}" for i in range(1, 21)},  # 20个章节
        }
    )
    
    mock_show_manga_details = mock.Mock(return_value=mock_manga)
    mock_print = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.show_manga_details", mock_show_manga_details)
    monkeypatch.setattr("builtins.print", mock_print)
    
    info_command(info_args)
    
    # 验证 show_manga_details 被调用
    mock_show_manga_details.assert_called_once_with("12345")
    
    # 验证打印了基本信息和章节信息
    assert mock_print.call_count > 5  # 至少打印了ID、标题、作者等


def test_info_command_manga_not_found(info_args, monkeypatch):
    """测试信息命令（漫画不存在）"""
    mock_manga = MangaInfo(cid="12345", title=None)
    
    mock_show_manga_details = mock.Mock(return_value=mock_manga)
    mock_print = mock.Mock()
    
    monkeypatch.setattr("mhg_dl.main.show_manga_details", mock_show_manga_details)
    monkeypatch.setattr("builtins.print", mock_print)
    
    info_command(info_args)
    
    # 验证打印了"未找到"信息
    mock_print.assert_called_once_with("Comic not found.")
