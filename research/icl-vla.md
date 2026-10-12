# 具备 ICL 能力的 VLA · 文献检索

检索与核对日期：**2026-10-09**。依据作者论文、项目页及会议论文集，核对了下列工作的上下文接口、训练与部署的区别、机器人证据。此页是专题阅读清单；逐篇全文精读、PDF 和原图归档状态以正式论文笔记为准。

**正式入库完成**：下列五篇已依次编号为 019–023，每篇保存全文、总览图、方法图和来源记录；笔记库累计 **24 篇**。[全部论文目录](../index.html)。MEM 与补充阅读尚未在本次作为正式全文笔记归档。

## 如何判断 ICL

本次重点关注：**部署时策略参数保持固定，利用新提供的示范或交互经验改变动作预测**。离线训练模型学会使用上下文，与测试时是否更新参数，是两个问题。检索库中的示范总数也不等于一次送入模型的示范数。

需要分别核对：上下文包含图像、动作、结构化文字还是自身历史；适应的是新任务、新物体、新场景还是失败后的策略；ICL 发生在动作策略还是高层代理。单独报告上下文消融和任务划分，比只看整体成功率更有解释力。

## 优先阅读 · 示范驱动的动作策略

### 1. RICL · CoRL 2025

[019 · 正式全文笔记](../ricl.html) · [原始 PDF](https://arxiv.org/abs/2508.02062v1) · [原图与来源](../assets/019-ricl/manifest.json)。

**Adding In-Context Adaptability to Pre-Trained Vision-Language-Action Models**。

- **接口与机制**：对 π₀-FAST 做离线后训练，使它利用检索到的观测、状态和动作片段；新任务的 10–20 条机器人示范成为检索库。
- **ICL 证据**：真机评估使用每任务 20 条示范、10 次测试，测试适应过程不更新参数。八个任务的完整成功率由基础模型的 2.5% 提升至 31.25%；额外目标任务微调是另一设置，不能混入 ICL 成绩。
- **阅读价值**：直接回答如何给现有 VLA 增加上下文适应能力；适合作为起点。作者项目页提供代码、模型和数据入口。[论文方法与实验](https://arxiv.org/html/2508.02062v1) · [作者项目页](https://ricl-vla.github.io/)。

### 2. ReCAP · 2026-06

[020 · 正式全文笔记](../recap.html) · [原始 PDF](https://arxiv.org/abs/2606.15631v1) · [原图与来源](../assets/020-recap/manifest.json)。

**Retrieve, Don't Retrain: Extending Vision Language Action Models to New Tasks at Test Time**。

- **接口与机制**：离线用目标机器人与较便宜的来源具身示范学习检索条件策略，随后冻结；新增任务通过扩展示范池，每个控制步检索相关轨迹。检索动作提供粗运动，模型预测具身差异的残差。
- **证据与范围**：包含 PushT、RoboTwin 2.0 和真机；真机新增两个保留任务，各提供 10 条人手示范。主要实现基于 Cosmos Policy 的 WAM，也检验标准 VLA；更换未见机器人具身仍需要微调。
- **关键限制**：人手输入需要可用的状态—动作轨迹与共同末端动作空间，不能直接等同于任意 RGB 视频。对人类数据驱动的机器人适应尤其值得读。[论文](https://arxiv.org/html/2606.15631v1) · [作者项目与实现入口](https://recap-robot.github.io/)。

### 3. StellaVLA · 2026-08

[021 · 正式全文笔记](../stellavla.html) · [原始 PDF](https://arxiv.org/abs/2608.11671v1) · [原图与来源](../assets/021-stellavla/manifest.json)。

**In-Context Structured Demonstration for Generalizable Vision-Language-Action Models**。

- **接口与机制**：一条检索示范被转为任务计划、子目标、2D/3D 运动文字；Qwen3-VL 骨干联合学习动作与空间语言。部署保留示范上下文，直接使用动作专家，无需逐步生成推理文字。
- **ICL 证据**：固定检查点在 LIBERO 上，正确、缺失、错误任务示范分别为 98.8%、62.4%、44.9%，显示动作策略确实依赖上下文。
- **机器人与边界**：AgileX Piper 真机操作，并接入人手、XR、机器人结构化示范；三种来源的一致性分析主要是单步预测，不能扩写为全部闭环结果等价。适合研究如何把人类示范压缩成可迁移的上下文。[论文方法与消融](https://arxiv.org/html/2608.11671v1)。

### 4. RA-VLA · ICML 2026

[022 · 正式全文笔记](../ra-vla.html) · [原始 PDF v2](https://arxiv.org/abs/2608.25585v2) · [原图与来源](../assets/022-ra-vla/manifest.json)。全文总结使用 **2026-10-07 更新的 arXiv v2**。

**Retrieval-Augmented VLA for Test-Time Adaptation**。

- **接口与机制**：用离线动作 DTW 对齐训练检索器，使检索依据行为相关性；再把专家片段通过交叉注意力接入动作头。缓存冻结 VLM 的片段特征，降低长上下文成本。
- **ICL 设置**：先离线训练检索器与适应接口，测试保留任务时固定参数。GR00T N1.5 为骨干；默认输入一个检索片段，真机每个保留任务的库包含四条专家示范。
- **证据与价值**：LIBERO 与 UR5e 真机。适合研究“检索到相似画面”如何转化为“执行相关动作”，以及上下文接入动作专家的位置。[正式会议记录](https://proceedings.mlr.press/v306/jang26c.html) · [论文方法 v2](https://arxiv.org/html/2608.25585v2)。

### 5. ICI-VLA · 2026-09

[023 · 正式全文笔记](../ici-vla.html) · [原始 PDF](https://arxiv.org/abs/2609.07581v1) · [原图与来源](../assets/023-ici-vla/manifest.json)。

**In-Context Imitation with Spatiotemporally Aligned Demonstrations for Vision-Language-Action Models**。

- **接口与机制**：Qwen3-VL 直接输出数值动作文本；把长示范拆成微示范，以语义过滤和离线 DTW 监督训练 RD-Encoder，检索匹配执行阶段的上下文。训练中的 Target Action Masking 减少对精确动作前缀的依赖。
- **ICL 设置**：推理冻结策略和检索器，默认使用三条短示例；测试检索不需要查询的目标动作。
- **证据与边界**：LIBERO、RoboTwin 2.0，以及四项双臂 Aloha 真机任务。轨迹划分独立，但部分基准的任务语义仍可能重复；不能把所有分数解释成完全未见技能学习。本次未确认公开实现入口。[论文与评估协议](https://arxiv.org/html/2609.07581v1)。

## 另一种 ICL · 通过自身交互经验调整动作

### MEM · 2026-03

**Multi-Scale Embodied Memory for Vision Language Action Models**。

在 π₀.₆ 中组合短期视频记忆与长期语言记忆。与上面的示范检索不同，适应线索可以是机器人自己刚才的失败：抓筷子时调整抓取高度，开冰箱时改换开门策略。作者先离线训练包含失败与人类纠正的轨迹，再测试运行中的策略调整；不能解释成完全无需训练就自动获得该能力。包含单臂、双臂、移动机器人真机实验。[论文 IV-B 与任务细节](https://arxiv.org/html/2603.03596v2)。

## 补充阅读 · 方法基础与系统层 ICL

### ICRT · 2024 年初稿

**In-Context Imitation Learning via Next-Token Prediction**：将遥操作的图像—本体状态—动作轨迹作为前缀，以因果 Transformer 预测动作，Franka 真机新任务适应不更新参数。它不依赖语言数据，适合作为机器人 ICL 的机制参照。[作者项目页](https://icrt.dev/) · [论文](https://arxiv.org/abs/2408.15980)。

### KAT · RSS 2024

**Keypoint Action Tokens Enable In-Context Imitation Learning in Robotics**：把视觉关键点与动作轨迹编码成文本 token，使用文本预训练 Transformer 做少样本模仿，有真机证据。它是关键点表示加通用 LLM 的路线，可帮助思考人—机器人动作接口。[论文](https://arxiv.org/abs/2403.19578)。

### BPP · 2026

**Behavior Prompting Policy: Demonstrations as Prompts for Manipulation**：将单条感觉运动示范作为 behavior prompt，通过上下文编码器和动作扩散解码器适应未见绘图与组合操作；作者强调训练任务多样性的重要性。主要是示范条件视觉动作策略，语言作为对照接口。[论文](https://arxiv.org/abs/2606.30457) · [作者项目与评测说明](https://behavior-prompting.github.io/)。

### RAEA · CVPR 2024

**Retrieval-Augmented Embodied Agents**：从多模态策略记忆库检索观测、指令、状态和动作，经交叉注意力生成动作，有仿真与 Franka 实验。是检索条件控制的早期相关工作；其少样本训练、未见物体和新任务 ICL 设置应分别核对。[正式论文](https://openaccess.thecvf.com/content/CVPR2024/html/Zhu_Retrieval-Augmented_Embodied_Agents_CVPR_2024_paper.html)。

### RV-ICL · 2026-10-05

**Recursive Video In-Context Learning for Agentic Robot**：将单条视频示范构建为可按需访问的子事件层级，由高层代理在规划和执行中查询，再调用冻结的 VLA。论文证据来自 LIBERO-PRO / LIBERO-Plus；这里的 ICL 主要发生在代理层，不能据此说低层 VLA 自身获得了示范归纳能力。[论文](https://arxiv.org/abs/2610.06843)。

### Skild S1 · 公司研究发布

作者发布展示以视频示范指定未见操作任务、固定权重执行的机器人 ICL。页面说明任务由视频而非语言指定，因此作为广义机器人基础策略的补充；本次依据公司研究博客，复现细节和训练方法的证据层级应与公开论文区分。[Skild 官方研究发布](https://skild.ai/blogs/s1)。

## 做研究时建议一起读

**When Does Retrieval Help? A Study of In-Context Adaptation in Vision-Language-Action Models**（2026-10-04）在 RICL 框架下比较图像、图像加状态、VLA 特征及随机检索。LIBERO 的 25 个任务各测试 10 次；没有检索表示始终领先，检索质量诊断也不可靠地预测控制表现。它适合帮助设计检索消融，而不是作为新的基础 VLA。[论文](https://arxiv.org/html/2610.05492v1)。

## 与现有全身智能笔记的联系

**我的阅读建议**：先读 RICL 建立机制，再读 ReCAP 与 StellaVLA 对比“轨迹上下文”和“结构化语义上下文”，随后读 RA-VLA / ICI-VLA 的检索与动作接入；若目标是运行中自纠错，再读 MEM。

对 [KODA](../papers/002-koda.md) 而言，可以进一步研究其 canonical motion 和机器人观测是否能作为测试时上下文，而不仅作为训练数据。这是阅读者提出的研究方向；上述机械臂操作结果不能直接外推为人形全身平衡与接触任务已经具备同样能力。

## 修订记录

- **2026-10-09**：建立专题清单，核对五条示范驱动路线、MEM 的交互适应及相关方法。正式全文总结目录仍为 18 篇，本清单单独保存。
