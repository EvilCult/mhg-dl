# mhg-dl
[![PyPI Version](https://img.shields.io/pypi/v/mhg-dl.svg)](https://pypi.org/project/mhg-dl/)
[![GitHub stars](https://img.shields.io/github/stars/evilcult/mhg-dl.svg?style=social&label=Stars)](https://github.com/evilcult/mhg-dl/stargazers)
[![License](https://img.shields.io/pypi/l/mhg-dl.svg)](https://github.com/evilcult/mhg-dl)

**mhg-dl**：又一个 [manhuagui](https://www.manhuagui.com/) 的简易漫画抓取与下载工具  

提供漫画搜索、抓取、解析和下载功能。支持指定分类下载, 及跳过指定章节下载。



---

## 功能概览

- 搜索漫画
- 抓取漫画基本信息：标题、封面、作者  
- 解析漫画章节列表并支持过滤（全部 / 指定类型 / 跳过章节）  
- 下载漫画（封面 + 章节划分内容）并按本地目录保存  

---

## TODO

- [x] 漫画规则分析
- [x] 漫画下载, 分类下载, 跳过章节
- [x] 搜索漫画
- [x] 发布文件包
- [ ] 搜索详细信息
- [ ] 指定目录
- [ ] 指定下载章节

---

## 安装
```bash
uv tool install mhg-dl
# or
pip install mhg-dl
```

## 使用
```bash
# 帮助
mhg-dl -h

# 搜索漫画 e.g. 鬼灭之刃
mhg-dl search 鬼灭之刃

# 取得所有章节
mhg-dl get 19430

# 只下载单行本
mhg-dl get 494 -t 单行本

# 只下载单行本 且从20卷开始下载
mhg-dl get 494 -t 单行本 -s 第20卷
```

---
## 构建

```bash
git@github.com:EvilCult/mhg-dl.git

cd mhg-dl

uv sync

uv run -m mhg_dl.cli -h

uv build

uv tool install dist/*****.whl
```





> PS: 不想重复造轮子,但是,总有但是...
> 下载文件总有各种各种保存的格式, 遇上柯南这种100多卷的, 每次一更新要从头下,就不太能接受.