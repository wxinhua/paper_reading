# 维护笔记库

## 修改已有笔记

编辑 `papers/NNN-name.md` 并提交。网站会重新生成阅读页；HTML 是生成结果，不需要手动修改。

如果修改了一句话理解、标题、分类或标签，同时更新 `library.json` 中的对应记录，并更新 `updated_on`。正文变化在笔记末尾记录日期、原因和版本依据。

## 新增论文

1. 按全库下一个编号创建笔记，参考 [template.md](template.md)。
2. 在 `assets/NNN-name/` 保存作者的总览图、方法图和 `manifest.json`。记录原论文地址、版本、PDF 页码、原图注和图片校验值。
3. 在 `library.json` 的 `papers` 追加记录，至少填写 `id`、`short_title`、`title`、`read_on`、`note_path`、`reader_path`、`library_summary`、`category`、`tags` 和 `sources`。
4. 全身智能论文选择一个 `subcategory`：`brain-models`、`motion-control` 或 `data-and-evaluation`；跨模块工作补充 `related_subcategories` 和 `classification_reason`。ICL-VLA 使用独立 `category: icl-vla`。
5. 更新 README 的目录、篇数、图片数和整理日期。
6. 执行 `python3 tools/build_site.py`，检查成功后提交到 `main`。GitHub Actions 会自动发布网页。

`reader_path` 使用根目录的文件名，例如 `new-paper.html`；笔记内图片用相对路径，例如 `../assets/025-new-paper/fig-01-overview.png`。全文用公开原论文链接，图片保留作者原图和原图注。

## 首次启用在线阅读

在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。

之后 `main` 分支更新自动发布。也可在 **Actions → Build and publish paper library → Run workflow** 手动运行。成功后访问 README 顶部的在线目录。

## 阅读与证据约定

- 原论文事实附来源；个人解释和推断明确标注。
- 实验记录平台、真机 / 仿真、任务、成功定义、样本量和测试条件。
- 没有公开的数字写“未报告”；不由视频推算成功率。
- 论文更新版本时记录改动原因。Being-M0.7 当前只依据 2026-10-08 arXiv v1。
- 分类按主要贡献确定一个主子类，关联方向不重复计数。

