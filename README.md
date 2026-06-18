# GitHub Trending Daily

> 每日自动抓取 GitHub Trending，生成精美简报，推送到 GitHub Pages

## 站点

**在线浏览**: [https://lph12168x.github.io/GitHub-Trending-Daily/](https://lph12168x.github.io/GitHub-Trending-Daily/)

## 内容

每日 10:00 自动执行，产出：

| 格式 | 说明 |
|------|------|
| `github-trending-YYYY-MM-DD.md` | Markdown 简报（排行榜 + 今日看点 + 语言分布） |
| `github-trending-YYYY-MM-DD.html` | 单文件 HTML 简报（暗色 GitHub 风格，内联样式） |
| `index.html` | GitHub Pages 首页（日报卡片网格，日期/Top3/总 Stars） |

## 数据来源

- [GitHub Trending](https://github.com/trending) — 全球热门开源项目
- 语言分布、Stars 增长、今日看点等统计均从 Trending 页面提取

## 自动化

由 [WorkBuddy](https://www.codebuddy.cn/) 定时任务驱动，流程：

1. 抓取 GitHub Trending 页面
2. 解析数据，生成 MD + HTML 简报
3. 通过 `gen_site.py` 将 MD 转为独立 HTML，更新 `index.html`
4. 推送到本仓库 `main` 分支（Git Credential Manager OAuth 认证）

## 目录结构

```
├── index.html                           # GitHub Pages 首页
├── github-trending-2026-06-09.md        # 06-09 Markdown 简报
├── github-trending-2026-06-09.html      # 06-09 HTML 简报
├── github-trending-2026-06-10.md
├── github-trending-2026-06-10.html
├── ...
└── README.md                            # 本文件
```

## 本地运行

如需手动生成 HTML 站点：

```bash
python gen_site.py
# 输出：index.html + 所有 github-trending-YYYY-MM-DD.html
```

## 许可

数据来源于 GitHub 公开页面，仅供学习参考。
