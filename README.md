# mhg-dl

**简体中文名**：mhg-dl — 一个针对 [manhuagui](https://www.manhuagui.com/) 的简易漫画抓取与下载工具  

mhg-dl 提供漫画搜索、抓取、解析和下载功能。

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
- [ ] 搜索详细信息
- [ ] 发布文件包

---

## 安装

```bash
git@github.com:EvilCult/mhg-dl.git

cd mhg-dl

uv sync

```

## 使用(暂时)
```bash
# 搜索漫画 e.g. 鬼灭之刃
uv run -m mhg_dl.cli search 鬼灭之刃

# 取得所有章节
uv run -m mhg_dl.cli get 19430

# 只下载单行本
uv run -m mhg_dl.cli get 494 -t 单行本

# 只下载单行本 且从20卷开始下载
uv run -m mhg_dl.cli get 494 -t 单行本 -s 第20卷
```




> PS: 不想重复造轮子,但是,总有但是...
> 下载文件总有各种各种保存的格式, 遇上柯南这种100多卷的, 每次一更新要从头下,真是遭不住!!!