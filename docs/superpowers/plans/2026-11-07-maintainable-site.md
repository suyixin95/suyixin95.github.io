# Maintainable Personal Site Implementation Plan

**Goal:** 本地只需修改内容文件即可持续维护个人网站。
**Architecture:** 保留 Jekyll / GitHub Pages；集中公共资料，论文单一来源；削减主题与演示代码。
**Tech Stack:** Jekyll、Liquid、Markdown、CSS；Python 内容和输出检查。
**Spec:** `docs/architecture.md`

## Global Constraints

- 保留中英文真实内容、五篇已有论文摘要及旧 permalink。
- 原始源码 ZIP 作为可恢复基线；不创建伪装成远端历史的 Git 仓库。
- 保留 CNAME，沿用 GitHub Pages 分支发布；本次不推送代码。
- 内容检查给出文件和字段位置；完整构建在 CI 执行。

## Tasks

- [x] 内容数据与检查：先添加真实目录 fixture 的缺字段、坏日期、重复路由、缺图测试；实现 `check_content.py`；迁移 profile 和 publication 元数据；运行 `python -m unittest discover -s tests` 与 `python scripts/check_content.py`。
- [x] 精简渲染：一个公共布局、一个论文布局、资料和论文条目 include；普通 CSS，移动布局与打印；保留旧地址。
- [x] 删除示例：在完整原始 ZIP 可恢复前提下移除无引用模板、示例内容、字体、JS 打包、地图和 Notebook；检查剩余引用。
- [x] 更新维护流程：README 更新入口、Windows 预览、检查、Git 提交和恢复；CI 内容检查、Jekyll build 和输出链接检查。
- [x] 验证交付：运行本机可用检查；记录构建限制；生成可应用到真正 Git 克隆的补丁，核对应用后内容和交付目录完全一致。

## Verification note

The Python content and built-site validators have 12 passing unit tests. The current workspace lacks a complete Ruby executable; the GitHub Actions job will run the authoritative Jekyll 3.9.5 build with Ruby 3.3. The local `check_site.py` negative path is covered by fixtures, while a full `_site` check awaits a real build.
