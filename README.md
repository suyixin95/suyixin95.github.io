# 苏一新的个人网站

这是一个精简的 Jekyll 静态网站，部署在 GitHub Pages，域名为 `suyixin.site`。日常更新以本地 Markdown / YAML 文件为主，不需要 npm、数据库或管理后台。

## 日常更新改哪里

| 要更新什么 | 修改文件 |
| --- | --- |
| 姓名、学位、头像、邮箱、地点、当前公司及职位、现职介绍、社交链接、微信二维码 | `_data/profile.yml` |
| 首页个人介绍、研究兴趣 | `_pages/about.md` |
| 教育、历史工作、科研项目、专利、奖励、技能 | `_pages/cv.md` |
| 新增或修改一篇论文 | `_publications/` 中对应的 Markdown 文件 |
| 主导航的顺序或名称 | `_data/navigation.yml` |
| 页面外观、手机布局、打印样式 | `assets/css/site.css` |
| 域名、构建配置 | `_config.yml`；更换域名还要同步 `CNAME` 和 DNS |

资料文件会自动同步到侧栏、首页现职介绍、简历现职、联系页和搜索摘要。`updated_on` 是**内容更新日期**，请在更新资料时一起修改。不会用每次部署时间冒充资料更新时间。

长篇经历继续写 Markdown。资料中的中英文是两份明确的内容，请同时更新。现有 `Chief Engineer / 高级工程师` 沿用原文，没有擅自重新翻译；历史科研项目中的“至今”也需要你自己核对结束时间。

### 换工作或调整职位

1. 将此前任职经历记入 `_pages/cv.md` 的历史工作部分，补上实际结束时间。
2. 修改 `_data/profile.yml` 的 `current`（公司、链接、中英文职位、开始年月、中英文工作内容）。
3. 如研究方向也变了，修改 `_pages/about.md` 的研究兴趣；更新 `updated_on`。

### 新增论文

在 `_publications/` 新建有意义的文件名，例如 `2027-short-title.md`。以下只是格式示例，请填写真实内容后再发布：

```yaml
---
title: "论文标题"
permalink: /publication/2027-short-title/
year: 2027
category: manuscripts
venue: "期刊或会议名称"
citation: "完整引用信息"
selected: true
---

英文摘要。

**中文摘要：** 中文摘要。
```

- `category`：期刊填 `manuscripts`，会议填 `conferences`。
- `selected: true`：自动进入简历代表作列表；不需要在 CV 再抄一遍。
- `paperurl`：可选，使用真实的 HTTPS 论文地址；不知道时直接省略，不放占位链接。
- `date`：可选，只有知道准确日期时才填 `YYYY-MM-DD`；只知道年份就只填 `year`。
- `note`：可选，注明已确认的奖项等信息。
- 标题改变时通常无需改 `permalink`，避免别人收藏的链接失效。旧论文保留原地址，文件名已整理。

YAML 用空格缩进，带冒号的文字用引号包起来；`true` / `false` 不加引号。页面列表会自动按年份倒序更新。

## 本地检查和预览（Windows）

一次性准备：安装 **Ruby 3.3 + Devkit**（RubyInstaller 官方版本）和 **Python 3.10 或更新版本**。确保 `ruby`、`bundle`、`python` 能在 PowerShell 中运行。进入包含本 README 的目录。

```powershell
bundle config set --local path vendor/bundle
bundle install
python -m pip install -r requirements-dev.txt
```

首次 `bundle install` 会生成 `Gemfile.lock`。请把它一起提交，让后续本机和 CI 使用同一套依赖；不要把 `vendor/` 提交。

每次更新后：

```powershell
python scripts/check_content.py
bundle exec jekyll serve --livereload
```

浏览器打开 `http://127.0.0.1:4000`。修改 Markdown / YAML 后查看刷新结果；修改 `_config.yml` 则停止并重启预览。确认首页、简历、论文和联系方式，在窄窗口中也能正常阅读。

提交前完整检查：

```powershell
python -m unittest discover -s tests
python scripts/check_content.py
bundle exec jekyll build --strict_front_matter
python scripts/check_site.py _site
```

内容检查会报告缺少字段、无效日期、重复页面地址、缺失图片和导航错误。构建后的检查会验证站内链接、锚点和资源；不会联网检查第三方网站是否可用。

## 提交与部署

在真正的 Git 克隆中编辑后，先通过上述检查，再查看修改：

```powershell
git diff --check
git diff --stat
git status --short
```

确认差异后，选择本次修改文件提交。GitHub Pages 继续沿用仓库原有的分支发布方式；本次没有改变你的远端设置。新增的 `Check website` 工作流会在 push / pull request 时运行内容检查、Jekyll 构建及站内链接检查。

**注意：这个检查工作流不是部署工作流，也不会自动阻止独立的分支式 Pages 发布。** 建议在工作分支提交，确认 pull request 的检查为绿色后再合并到发布分支。将来如果希望“检查成功才部署”，可以单独改为 GitHub Actions 发布并在仓库 Pages 设置中切换来源。

如果拿到的是没有 `.git` 的源码快照，请不要重新初始化并强推覆盖远端历史。应先正常克隆原仓库，在新分支应用本次交付的 `maintenance.patch`，按交付说明检查后再提交。

## 架构和保留内容

- 内容、模板、样式分别在 `_data` / `_pages` / `_publications`、`_layouts` / `_includes`、`assets/css`。
- 只有 Jekyll、sitemap、redirect 插件和本地预览服务器；Python 的 PyYAML 只用于开发检查。
- 主要页面无需 JavaScript，手机导航直接显示，深色模式跟随系统，简历支持浏览器打印为 PDF。
- `/portfolio/` 和旧微信详情页跳转到 `/contact/`；原论文地址、`/about/`、`/about.html` 和 `/resume` 继续可用。
- 原始五篇论文摘要、个人照片、研究图片、二维码和真实履历保留；CV 中独有的一篇中文论文纳入统一目录。
- 示例博客、示例教学与演讲、演讲地图及其自动提交任务、示例 JSON 简历、评论服务、旧 npm/JS/Sass 打包、模板配图已移除。

完整审查依据见 [架构审查](docs/architecture.md)。原项目 MIT 许可证保留在 `LICENSE`。
