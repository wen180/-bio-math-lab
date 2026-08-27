# 📅 ROADMAP · 详细课程表

> 六阶段 × 周次的结构化课程表：**约 33 周核心课程**（Stage 00–05），Stage 05 完成后进入持续迭代。
>
> **使用规则**
> - 每周聚焦一个主题。**检验标准 = 过关条件**：做不到，就不进入下一周——宁可慢，不可虚进度。
> - 过关自测方法：合上所有材料，在白板上完成检验标准；可以让 AI 当考官，但答案自己给。
> - 教材的章节级映射与获取方式见 [references/](./references/README.md)。

## 总时间轴

| 阶段 | 周次 | 时长 |
|---|---|---|
| Stage 00 · 数学与编程基础 | W1–W5 | 5 周 |
| Stage 01 · 动力学系统 | W6–W12 | 7 周 |
| Stage 02 · 随机过程 | W13–W17 | 5 周 |
| Stage 03 · 空间与多尺度 | W18–W22 | 5 周 |
| Stage 04 · 数据驱动推断 | W23–W28 | 6 周 |
| Stage 05 · AI×科学 | W29–W33 → 持续迭代 | 5 周 + ∞ |

---

## Stage 00 · 数学与编程基础（W1–W5）

**目标**：把数学捡回来并打通 Python 科学栈，以 logistic 生长模型完成第一次"假设 → 方程 → 求解 → 拟合"的完整闭环。
**教材**：Khan Academy（Calculus / Statistics）·《Python for Data Analysis》前几章 · 3Blue1Brown《线性代数的本质》

| 周次 | 主题 | 教材章节 | 检验标准（过关条件） |
|---|---|---|---|
| W1 | 微积分 I：导数、链式法则、定积分——建立"变化率"语言 | Khan Academy · Calculus（导数与应用单元） | 能从 dN/dt = rN 出发独立推导指数增长解析解；能逐项说出 logistic 方程中 r、N、K 的生物学含义 |
| W2 | 微积分 II：Taylor 展开与线性化、指数增长/衰减 | Khan Academy · Calculus（积分单元选看）；3B1B 微积分本质（选看） | 能在不动点附近做 Taylor 展开并解释线性化为何足以判断局部稳定性；能推导指数衰减的半衰期公式 |
| W3 | 线性代数：矩阵运算、特征值 / 特征向量 | 3B1B《线性代数的本质》Ch.1–10；《Python for Data Analysis》Ch.4（NumPy） | 能手算 2×2 矩阵的特征值，并说清特征值实部符号如何决定系统长期行为；能用 `numpy.linalg` 验证手算结果 |
| W4 | 概率统计：随机变量、常见分布、期望 / 方差、最大似然估计 | Khan Academy · Statistics and Probability（核心单元） | 能推导泊松分布作为二项分布的极限；能写数值实验验证中心极限定理；能对一组数据手推正态均值的 MLE |
| W5 | Python 科学栈闭环 + 里程碑 | 《Python for Data Analysis》Ch.2–3；NumPy / SciPy / matplotlib 官方 Quickstart | **里程碑 `stage00-logistic`**：logistic 解析解、Euler 与 RK45 数值解、带噪声数据拟合，三线同图 + 一句话结论 |

---

## Stage 01 · 动力学系统（W6–W12）

**目标**：掌握 ODE 定性分析（不动点、稳定性、分岔、振荡），能独立分析合成生物学两大经典回路。
**教材**：Strogatz《Nonlinear Dynamics and Chaos》Ch.1–6, 8 · Alon《An Introduction to Systems Biology》Ch.2–5

| 周次 | 主题 | 教材章节 | 检验标准（过关条件） |
|---|---|---|---|
| W6 | 一维流与不动点：几何直觉、稳定性 | Strogatz Ch.1–2；Alon Ch.2 | 能在相线（phase line）上画向量场并分类不动点；能把自抑制基因（negative autoregulation）写成 ODE 并定性分析 |
| W7 | 分岔：saddle-node、transcritical、pitchfork | Strogatz Ch.3 | 能解释 cooperative binding（Hill 系数 > 1）如何让基因开关产生 saddle-node 分岔；能手绘分岔图 |
| W8 | 二维线性系统：分类与相平面 | Strogatz Ch.5 | 能用迹–行列式（trace–determinant）平面分类全部 2×2 线性不动点类型 |
| W9 | 相平面分析：nullclines 与 toggle switch | Strogatz Ch.6；Alon Ch.3；Gardner et al. 2000 | 能徒手画出 toggle switch 的两条 nullcline，解释双稳态与滞后（hysteresis）；能数值复现其分岔图 |
| W10 | 极限环：为什么振荡需要二维 | Strogatz Ch.7 | 能解释一维自治系统不可能振荡而二维可以；能举一个生物振荡例子并说明其环路的必要条件 |
| W11 | Hopf 分岔与 repressilator | Strogatz Ch.8；Elowitz & Leibler 2000 | **能解释 repressilator 振荡的参数条件**（强协同、足够表达量、降解率匹配），并数值验证"降低 Hill 系数则振荡消失" |
| W12 | 里程碑项目周 | Alon Ch.4–5（motif 视角回顾） | **里程碑 `stage01-dynamics`**：toggle switch 双稳态分析 + repressilator 振荡条件扫描，报告一句话结论 |

---

## Stage 02 · 随机过程（W13–W17）

**目标**：理解细胞是低拷贝数的随机系统；掌握化学主方程与 Gillespie 直接法，能模拟并分析基因表达噪声。
**教材**：Gillespie 1977 (J. Phys. Chem.) · Wilkinson《Stochastic Modelling for Systems Biology》选章

| 周次 | 主题 | 教材章节 | 检验标准（过关条件） |
|---|---|---|---|
| W13 | 从质量作用到化学主方程（CME） | Wilkinson Ch.1（随机 vs 确定性建模） | 能解释 CME 与确定性速率方程的关系，以及低拷贝数时随机性为何不可忽略 |
| W14 | Gillespie 直接法：推导与算法 | Gillespie 1977 | 能推导 propensity function 与两个核心随机量（等待时间、下一个反应索引）；能手写 SSA 伪代码 |
| W15 | SSA 实现 + 简单基因表达 | Wilkinson 选章；Elowitz et al. 2002 | 能实现 SSA 模拟基本基因表达，统计均值 / 方差并与 ODE 解对比；能说清泊松近似何时失效 |
| W16 | 两态启动子与 bursting 噪声 | Wilkinson 选章 | 能推导两态启动子模型的平均表达量与方差；能解释 translational bursting 如何放大噪声（Fano factor > 1） |
| W17 | 里程碑项目周 | — | **里程碑 `stage02-noise`**：SSA 实现 + 噪声–参数关系分析，结论一句话 |

---

## Stage 03 · 空间与多尺度（W18–W22）

**目标**：从均匀混合假设走向空间；掌握反应扩散方程与图灵不稳定性，数值复现发育模式形成。
**教材**：Murray《Mathematical Biology II》图灵模式相关章节

| 周次 | 主题 | 教材章节 | 检验标准（过关条件） |
|---|---|---|---|
| W18 | 扩散方程：从随机游走到 Fick 定律 | Murray II（空间建模导论章节） | 能从一维随机游走推导扩散方程；能解释特征长度 √(Dt) 对细胞内信号扩散的含义 |
| W19 | 反应扩散系统与线性稳定性分析 | Murray II（反应扩散章节） | 能对两物种反应扩散系统做含扩散项的线性稳定性分析，写出色散关系（dispersion relation） |
| W20 | 图灵不稳定性 | Murray II（图灵模式章节） | 能推导图灵不稳定性的参数条件（抑制剂扩散显著快于激活剂），并解释"局部激活–长程抑制" |
| W21 | 数值模拟斑图 + 参数扫描 | 同上 | 能数值模拟图灵斑图（Schnakenberg 或 Gierer–Meinhardt），扫描参数观察条纹 ↔ 斑点转变 |
| W22 | 里程碑项目周 | — | **里程碑 `stage03-pattern`**：斑图模拟 + 参数相图，结论一句话 |

---

## Stage 04 · 数据驱动推断（W23–W28）

**目标**：从"解正问题"转向"解反问题"——给定带噪声的数据，推断模型参数并量化不确定性。
**教材**：van de Schoot et al. 2021 贝叶斯教程（或《Statistical Rethinking》选章）

| 周次 | 主题 | 教材章节 | 检验标准（过关条件） |
|---|---|---|---|
| W23 | 贝叶斯基础：先验、似然、后验 | van de Schoot et al. 2021 前半；Statistical Rethinking Ch.2–3 | 能用贝叶斯定理手算一个离散参数的后验；能解释先验如何被数据逐步更新 |
| W24 | MCMC 原理：Metropolis–Hastings | 同上 | 能推导 MH 接受率公式，并解释详细平衡（detailed balance）为何保证收敛到后验 |
| W25 | 手写采样器 + 收敛诊断 | Statistical Rethinking Ch.3 / 9 选读 | 能从零实现 MH 采样器；能用 trace plot 与 R-hat 判断收敛，解释 burn-in 的作用 |
| W26 | ODE 参数推断实战 | van de Schoot et al. 2021 后半 | 能对 logistic 模型的带噪时间序列做贝叶斯参数估计，报告后验均值与 90% 可信区间 |
| W27 | 模型比较与后验预测检验 | Statistical Rethinking 选章 | 能用后验预测检验（posterior predictive check）暴露模型 misfit；能比较两个嵌套模型并说明理由 |
| W28 | 里程碑项目周 | — | **里程碑 `stage04-inference`**：从（合成或真实）数据恢复 ODE 参数全流程，结论一句话 |

---

## Stage 05 · AI×科学（W29–W33 → 持续迭代）

**目标**：让 AI 在数学约束下工作——PINN 把方程写进损失函数，代理模型把计算预算花在刀刃上。核心 5 周入门，之后进入自由选题持续迭代。
**教材**：Raissi et al. 2019 (JCP) · Karniadakis et al. 2021 (Nat. Rev. Phys.)

| 周次 | 主题 | 教材章节 | 检验标准（过关条件） |
|---|---|---|---|
| W29 | PINN 原理 | Raissi et al. 2019 | 能写出 PINN 损失函数（数据项 + PDE 残差项 + 边界 / 初值项），解释每一项的作用及权重失衡的后果 |
| W30 | 实现 PINN 解 ODE | 同上（对照官方开源代码） | 能用 PyTorch 实现 PINN 求解 logistic 方程，与解析解同图对比并量化误差 |
| W31 | 代理模型（surrogate）与主动学习 | Karniadakis et al. 2021 | 能画出 surrogate + 主动学习的工作流图，说明相比直接数值解在参数扫描中省在哪里 |
| W32 | 软约束 vs 硬约束 | 同上 | 能区分软约束（损失项）与硬约束（网络结构内嵌守恒律）的差别与代价，各举一个生物学场景 |
| W33+ | 里程碑项目 + 自由迭代 | — | **里程碑 `stage05-pinn`**：用 PINN 求解反应扩散方程并与有限差分对比；此后自由选题（如 SINDy、数据同化、面向实验设计的数学工具）持续迭代 |

---

## 机动与缓冲

- 单周内容卡壳超过 1 周，允许顺延，但**检验标准不打折**。
- 每完成一个阶段，回 [progress.md](./progress.md) 复盘：掌握度 ≤ 2 的概念列入下一阶段的复习清单。
- Stage 05 没有终点：目标是从"学习者"过渡为"用数学约束 AI、为 AI 打造科学工具的实践者"。
