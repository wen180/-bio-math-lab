# 🧫 bio-math-lab

> **从零到 AI×科学的细胞生物学数学建模学习档案。**
> 一个细胞生物学背景的学习者，系统补足数学建模、走向建模 × 生物学交叉领域——所有推导、代码、踩坑与疑问都沉淀在这里。

[![Current Stage](https://img.shields.io/badge/Current_Stage-00_Foundations-blue)](./ROADMAP.md)
[![Milestones](https://img.shields.io/badge/Milestones-0%2F6-lightgrey)](./projects/)
![Method](https://img.shields.io/badge/Method-Derive_Verify_Log-orange)
[![Since](https://img.shields.io/badge/since-2026_08_27-green)](./progress.md)

---

## 为什么这样学：三条原则

本仓库的一切安排——课程顺序、AI 使用方式、检验标准——都从以下三条原则推导出来。

### 1. 建模真实世界

数学不是先学完再用，它是对真实生物系统的**压缩描述**。"细胞在有限营养下增长"这个生物学陈述，压缩之后就是 logistic 方程：

$$\frac{dN}{dt} = rN\left(1-\frac{N}{K}\right)$$

先对真实系统提出假设（状态变量是什么？谁与谁相互作用？速率由什么决定？），把假设翻译成方程，**再**谈计算。方程写下的一刻，模糊的直觉就变成了可检验、可证伪的陈述。所以本仓库每个数学概念都必须配一个生物学场景——映射关系见 [ROADMAP.md](./ROADMAP.md)。

### 2. 用数学约束 AI

AI 能在几秒内生成一段拟合代码或一页推导，但它不知道模型**应该**满足什么：量纲是否一致、质量是否守恒、参数是否落在生物学合理范围、解是否稳定。这些约束条件与验证标准来自数学模型与真实数据，**不来自 AI 的输出**。

> AI 是计算引擎，数学是方向盘与刹车。要为 AI 打造科学工具，前提是自己先掌握这套约束。

### 3. 第一责任人

可以借助 AI 讲解、评审、出题，但模型与代码的最终责任在自己。硬性标准只有一条：

> **合上答案，能在白板上独立重做。** 看不懂的推导与代码，不进入本仓库主线。

---

## 🔁 三步学习法（每次学习都遵循）

| 步骤 | 做什么 | 硬性要求 |
|---|---|---|
| ① **先推导** | 自己先推公式、先写代码 | 卡住也要先尝试 ≥ 30 分钟；把卡点原样记下来——卡点是最有价值的输入 |
| ② **再验证** | 交给 AI 评审、对照参考答案、做数值实验 | 对 AI 只要求"指出问题"，不要求"替我改好"；解析解与数值解必须画在同一张图上 |
| ③ **后记录** | 在 [progress.md](./progress.md) 追加一条记录 | 掌握度自评 1–5；**疑问不过夜** |

**疑问不过夜**的含义：每个疑问要么当次会话内解决，要么转化为下一次会话的第一个明确任务，不允许悬空。

---

## 🗺️ 六阶段路线总览

| 阶段 | 主题 | 核心数学工具 | 生物学场景 | 里程碑项目 |
|---|---|---|---|---|
| **Stage 00** | 数学与编程基础 | 微积分、线性代数、概率统计、Python 科学栈 | 细胞生长模型闭环 | `stage00-logistic`：解析解 + 数值解 + 数据拟合三线同图 |
| **Stage 01** | 动力学系统 | ODE、稳定性、分岔 | toggle switch、repressilator | `stage01-dynamics`：双稳态与振荡条件的数值证明 |
| **Stage 02** | 随机过程 | 化学主方程（CME）、Gillespie SSA | 基因表达噪声 | `stage02-noise`：SSA 实现 + 噪声–参数关系分析 |
| **Stage 03** | 空间与多尺度 | 反应扩散方程、图灵不稳定性 | 发育模式形成 | `stage03-pattern`：斑图模拟 + 参数相图 |
| **Stage 04** | 数据驱动推断 | 贝叶斯推断、MCMC | 从数据恢复参数 | `stage04-inference`：后验参数估计全流程 |
| **Stage 05** | AI×科学 | PINN、代理模型（surrogate model） | 数学约束的机器学习 | `stage05-pinn`：PINN 与传统数值方法对比 |

📅 完整课程表（周次 × 主题 × 教材章节 × 检验标准）见 **[ROADMAP.md](./ROADMAP.md)**：约 33 周核心课程 + Stage 05 持续迭代。

---

## 📁 目录结构

```text
bio-math-lab/
├── README.md        # 本文件：导航 + 学习哲学 + 方法论
├── ROADMAP.md       # 详细课程表：六阶段 × 周次 × 教材映射 × 检验标准
├── progress.md      # 学习日志：每条记录含掌握度自评与疑问
├── modules/         # 六阶段课程内容：讲义 + 练习 + 参考答案
│   ├── 00-foundations/
│   ├── 01-dynamics/
│   ├── 02-stochastic/
│   ├── 03-spatial/
│   ├── 04-inference/
│   └── 05-ai-science/
├── notes/           # 费曼式概念笔记（一个概念一个文件）
├── projects/        # 里程碑项目：能跑的代码 + 一页纸报告
└── references/      # 分阶段书单与资源（含获取方式提示）
```

---

## 🚀 快速开始：配合 TRAE / AI 的一轮学习会话（约 2 小时）

1. **读讲义（30–40 min）** — 打开 `modules/<阶段>/` 中当周讲义，跟着推导一遍，不跳步。
2. **做练习（40–50 min）** — 先自己写；卡住 ≥ 30 分钟才求助，求助时问"给我提示"，不问"给我答案"。
3. **AI 评审（15–20 min）** — 把自己的推导 / 代码交给 TRAE，评审指令模板：

   > "请只指出错误、量纲问题与潜在风险，**不要**给出修正后的完整代码。"

4. **记录（10 min）** — 在 [progress.md](./progress.md) 追加一条：学到了什么、掌握度几级、疑问是什么、下一步干什么。

常用指令模板（让 AI 保持陪练角色，而不是代劳）：

| 场景 | 指令模板 |
|---|---|
| 讲解 | "用费曼技巧讲 \<概念\>：先给直觉，再给公式，最后出一道检验题（先不给答案）" |
| 评审 | "只指出我推导中的错误与漏洞，不要替我完成" |
| 出题 | "就 \<概念\> 出 3 道由易到难的检验题，我做完再逐题给分与讲评" |

---

## 📊 当前状态

[![Stage 00](https://img.shields.io/badge/00_foundations-in_progress-blue)](./ROADMAP.md)
[![Stage 01](https://img.shields.io/badge/01_dynamics-not_started-lightgrey)](./ROADMAP.md)
[![Stage 02](https://img.shields.io/badge/02_stochastic-not_started-lightgrey)](./ROADMAP.md)
[![Stage 03](https://img.shields.io/badge/03_spatial-not_started-lightgrey)](./ROADMAP.md)
[![Stage 04](https://img.shields.io/badge/04_inference-not_started-lightgrey)](./ROADMAP.md)
[![Stage 05](https://img.shields.io/badge/05_AI_science-not_started-lightgrey)](./ROADMAP.md)

| 阶段 | 状态 | 里程碑 |
|---|---|---|
| Stage 00 · 数学与编程基础 | 🚧 进行中（2026-08-27 起） | ⬜ `stage00-logistic` |
| Stage 01 · 动力学系统 | ⏳ 未开始 | ⬜ `stage01-dynamics` |
| Stage 02 · 随机过程 | ⏳ 未开始 | ⬜ `stage02-noise` |
| Stage 03 · 空间与多尺度 | ⏳ 未开始 | ⬜ `stage03-pattern` |
| Stage 04 · 数据驱动推断 | ⏳ 未开始 | ⬜ `stage04-inference` |
| Stage 05 · AI×科学 | ⏳ 未开始（持续迭代型） | ⬜ `stage05-pinn` |

> 学习日志：[progress.md](./progress.md) · 课程表：[ROADMAP.md](./ROADMAP.md) · 书单：[references/](./references/)

---

*仓库地址：<https://github.com/wen180/-bio-math-lab> · 学习的持久载体始终是本 GitHub 仓库，内容随学习进度持续迭代。*
