# 全身智能 · Paper 笔记库

持续积累论文阅读记录，按 Motivation、方法、实验、结论整理，保留个人判断、证据边界和作者原始总览 / 方法图。

**[在线阅读目录](https://wxinhua.github.io/paper_reading/)** · [统一笔记模板](template.md) · [维护说明](CONTRIBUTING.md)

当前共 **32 篇**，保存 **87 张论文原图**。图片保留原图注，来源记录包含论文版本、页码、裁剪参数和校验值。编号按全库顺序累积。

## 分类

**Wholebody Intelligence · 27 篇**

- [大脑模型与任务策略 · 13 篇](https://wxinhua.github.io/paper_reading/#subcategory-brain-models)：VLA / VAM / WAM、视觉任务策略、文字动作生成、世界模型与高层规划。
- [运动控制与重定向 · 5 篇](https://wxinhua.github.io/paper_reading/#subcategory-motion-control)：GMT / WBC 类全身跟踪、关节控制、重定向 / IK 与部署时参考运动复用。
- [数据、基准与综述 · 9 篇](https://wxinhua.github.io/paper_reading/#subcategory-data-and-evaluation)：示范对齐与生成、仿真基础设施、评测与综述。

每篇按主要贡献确定一个主子类，跨模块工作标注关联方向，篇数不重复计算。分类是笔记库的组织判断。TextOp 属于文字动作生成；VIRAL、FetchMan 属于视觉任务策略，这个分组不把它们都称为基础 VLA。

**[ICL-VLA · 5 篇](https://wxinhua.github.io/paper_reading/#category-icl-vla)**：示范上下文条件下的视觉语言动作适应。另有[专题阅读清单](research/icl-vla.md)，不重复计入正式篇数。

## 论文笔记

- 001 · [Workhorse](papers/001-workhorse.md)
- 002 · [KODA](papers/002-koda.md)
- 003 · [SONIC](papers/003-sonic.md)
- 004 · [HumanoidArena](papers/004-humanoidarena.md)
- 005 · [WARP](papers/005-warp.md)
- 006 · [OpenHLM](papers/006-openhlm.md)
- 007 · [SIMPLE](papers/007-simple.md)
- 008 · [GRAIL](papers/008-grail.md)
- 009 · [HumanTracker](papers/009-humantracker.md)
- 010 · [WholeBodyWAM](papers/010-wholebodywam.md)
- 011 · [Humanoid Locomotion and Manipulation · 综述](papers/011-humanoid-survey.md)
- 012 · [EgoHumanoid](papers/012-egohumanoid.md)
- 013 · [HumanoidMimicGen](papers/013-humanoidmimicgen.md)
- 014 · [VIRAL](papers/014-viral.md)
- 015 · [FetchMan](papers/015-fetchman.md)
- 016 · [SynAgent](papers/016-synagent.md)
- 017 · [λ0 / HumanVerse-500](papers/017-human-pretraining.md)
- 018 · [TextOp](papers/018-textop.md)
- 019 · [RICL](papers/019-ricl.md)
- 020 · [ReCAP](papers/020-recap.md)
- 021 · [StellaVLA](papers/021-stellavla.md)
- 022 · [RA-VLA](papers/022-ra-vla.md)
- 023 · [ICI-VLA](papers/023-ici-vla.md)
- 024 · [Being-M0.7 · 10 月版](papers/024-being-m07.md)
- 025 · [VioLA](papers/025-viola.md)
- 026 · [HumanoidTTT](papers/026-humanoidttt.md)
- 027 · [EgoHumanoid-V2](papers/027-egohumanoid-v2.md)
- 028 · [Ropedia W0](papers/028-ropedia-w0.md)
- 029 · [VPP2](papers/029-vpp2.md)
- 030 · [LocoManiLab](papers/030-locomanilab.md)
- 031 · [SP-HLM](papers/031-sp-hlm.md)
- 032 · [Being-M0.5 / MotionCtrl](papers/032-being-m05.md)

## 更新方式

在 GitHub 中编辑 `papers/` 下的 Markdown 笔记，提交到 `main` 后，网页自动重新生成。新增论文时按[维护说明](CONTRIBUTING.md)追加笔记、图片和 `library.json` 记录。

本地使用 Python 3.10 或更新版本，无额外依赖：

```sh
python3 tools/build_site.py
```

生成的网页位于 `dist/`，可直接打开 `dist/index.html`；持续发布由 [.github/workflows/pages.yml](.github/workflows/pages.yml) 完成。

## 文件组织

- `papers/`：每篇独立笔记。
- `assets/`：论文原图及来源记录。
- `library.json`：标题、论文版本、分类、关联方向和目录信息。
- `research/`：专题阅读清单。
- `tools/`：生成阅读页、检查链接和构建网站。

阅读页通过作者 / arXiv / OpenReview 链接访问论文全文。本地 PDF 归档与 Zotero 关联信息单独保存。WholeBodyWAM 的归档来源未记录可核实的公开地址，笔记明确保留这一来源边界。

论文图片与论文内容的权利归原作者；各笔记和图像记录保留原始出处。论文事实与阅读者判断分开；不同实验协议下的成功率不直接排名。

最后整理：**2026-10-27**。

