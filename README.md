# mhg-dl

[![PyPI Version](https://img.shields.io/pypi/v/mhg-dl.svg)](https://pypi.org/project/mhg-dl/)
![Downloads](https://static.pepy.tech/badge/mhg-dl?x=42)


![Platform](https://img.shields.io/badge/platform-CLI-lightgrey)
![uv](https://img.shields.io/badge/built%20with-uv-5f43e9)
![ruff](https://img.shields.io/badge/lint-ruff-red)
[![License](https://img.shields.io/github/license/evilcult/mhg-dl.svg)](LICENSE)


[![GitHub stars](https://img.shields.io/github/stars/evilcult/mhg-dl.svg?style=social&label=Stars)](https://github.com/evilcult/mhg-dl/stargazers)


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
- [x] 搜索详细信息
- [x] 出错自动重试
- [x] 指定下载章节
- [x] 流式下载
- [x] 指定输出目录
- [x] 美化输出格式

---

## 安装
```bash
pip install mhg-dl
# or
uv tool install mhg-dl
```

## 更新
```bash
pip install --upgrade mhg-dl
# or
uv tool upgrade mhg-dl
```

## 使用
```bash
# 帮助
mhg-dl -h

# 搜索漫画 e.g. 鬼灭之刃
mhg-dl search 鬼灭之刃

# 查看漫画详细信息
mhg-dl info 19430

# 下载所有内容
mhg-dl get 19430

# 将漫画下载到指定目录 e.g. ~/Pictures
mhg-dl get 494 -t 单行本 -o ~/Pictures

# 仅下载 ‘单行本’ 分类的内容
mhg-dl get 494 -t 单行本

# 仅下载 ‘单行本’ 的 ‘第20卷’ 及以后内容
mhg-dl get 494 -t 单行本 -s 第20卷

# 仅下载 ‘单行本’ 的 ‘第20卷’
mhg-dl get 494 -t 单行本 -p 第20卷

# 显示完整信息, 推荐使用nohup时开启以记录log
mhg-dl get 494 -t 单行本 -v
```

---
## 构建

```bash
git clone git@github.com:EvilCult/mhg-dl.git

cd mhg-dl

uv sync

uv run -m mhg_dl.cli -h

uv build

uv tool install dist/*****.whl
```
