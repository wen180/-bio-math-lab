# 讲义 04 · Python 科学计算栈：把数学变成可运行代码

> **对应阶段**：Stage 00 · 第 5 周
> **前置要求**：会安装软件、会打开终端；**不需要**系统学过 Python（边用边学，本仓库只用到一个小子集）
> **阅读方式**：约 2 小时；每个代码块都在 Jupyter 里亲手运行并修改参数——**读代码不涨功力，改代码才涨**

---

## 0. 本讲要回答的三个问题

1. 为什么整个课程统一用 Python（而不是 MATLAB / R / Julia）？
2. 讲义 01–03 的数学——微分方程、矩阵指数、似然函数——分别对应哪几个函数调用？
3. "数值求解 ODE → 可视化 → 拟合参数"这条闭环工作流的最小可用版本长什么样？

---

## 1. 为什么是 Python

- **免费、开源、跨平台**：科学不应该是买得起许可证的人的特权；
- **生态最全**：NumPy / SciPy / Matplotlib 覆盖本课程 90% 需求；PyTorch / JAX 覆盖 Stage 05；BioPython、Scanpy（单细胞组学）覆盖生物学下游；
- **AI 时代的通用语**：你未来为 AI 打造科学工具（本仓库学习哲学第二条），大概率就在 Python 生态里做。

本课程的全部代码遵循同一约定：**Python 3.10+，只用 NumPy / SciPy / Matplotlib（Stage 04 增补 PyMC 或 emcee，Stage 05 增补 PyTorch）**。

### 1.1 环境安装

```bash
# 方案 A（推荐）：标准 venv + pip
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install numpy scipy matplotlib jupyter

# 方案 B：conda / miniconda
conda create -n biomath python=3.12 numpy scipy matplotlib jupyter
conda activate biomath
```

验证安装：

```bash
python -c "import numpy, scipy, matplotlib; print('numpy', numpy.__version__, '| scipy', scipy.__version__, '| matplotlib', matplotlib.__version__)"
```

---

## 2. NumPy：数组即向量 / 矩阵

### 2.1 核心思想：向量化（vectorization）

**逐元素操作整个数组，不写 for 循环**。这是 NumPy 的全部灵魂：

- 更快（C 底层实现）；
- 更短（一行顶五行）；
- **更接近数学**：`r * N * (1 - N/K)` 与黑板上的 $rN(1-N/K)$ 逐字符对应。

### 2.2 最小示例集（每个都跑一遍）

```python
import numpy as np

# 创建数组（讲义 02 的"状态向量"）
x = np.array([2.0, 3.0, 5.0])
t = np.linspace(0, 10, 101)          # 0 到 10，均匀 101 个点（含端点）—— 时间网格

# 向量化运算：整条曲线一次算完（讲义 01 的指数增长）
N0, r = 1000.0, 0.5
N = N0 * np.exp(r * t)               # 没有 for 循环！

# 切片：取出第 10 到 20 个时间点（Python 从 0 计数，左闭右开）
t_seg, N_seg = t[10:20], N[10:20]

# 矩阵（讲义 02 的"交互规则表"）
A = np.array([[0.0, 1.0],
              [-2.0, -3.0]])
A @ x                                 # 矩阵乘向量（@ 是矩阵乘法运算符）

# 广播（broadcasting）：标量与数组、行向量与列向量自动扩展对齐
K = 5000.0
N * (1 - N / K)                      # K 是标量，自动"广播"到每个元素

# 统计（讲义 03 的样本量）
counts = np.random.default_rng(42).poisson(lam=4.0, size=500)   # 模拟 500 个细胞的 mRNA 计数
counts.mean(), counts.var(), counts.std()                       # 均值、方差、标准差
```

### 2.3 两个新手陷阱

1. `A * B` 是**逐元素**乘，`A @ B` 才是矩阵乘法——写混了不报错但结果全错；
2. `np.arange(0, 1, 0.1)` 有浮点步长陷阱（长度可能不是 10）；**时间网格一律用 `np.linspace`**（长度精确可控）。

---

## 3. Matplotlib：让数据说话

### 3.1 标准五要素绘图流程

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4))     # 1. 画布与坐标区
ax.plot(t, N, label=r"$N_0 e^{rt}$")      # 2. 数据（r"" 字符串支持 LaTeX）
ax.plot(t, K * np.ones_like(t), "--", label=r"carrying capacity $K$")
ax.set_xlabel("time (h)")                 # 3. 轴标签（永远带单位！）
ax.set_ylabel("cell number N(t)")
ax.set_title("Exponential growth")         # 4. 标题
ax.legend()                                # 5. 图例
plt.show()
```

### 3.2 科研绘图的自我约束（本仓库统一约定）

- 轴标签**永远带单位**——审稿人（和未来的你）第一眼就看这个；
- 多条曲线必须能黑白区分：颜色 + 线型 + 图例三重保险；
- 一图一论点：图 caption 应能用一句话陈述"这张图证明了什么"；
- 数值解与解析解（或数据与拟合）**画在同一张图上**——这是仓库三步学习法中"再验证"环节的图形化体现。

### 3.3 常用图型速查

```python
ax.scatter(t_data, N_data, s=12, color="k", label="data")   # 数据点
ax.hist(counts, bins=20, density=True)                       # 分布直方图（讲义 03）
ax.semilogy(t, np.abs(N - N_ref))                            # 误差随时间（对数轴）
ax.imshow(pattern, cmap="viridis")                           # 2D 场（Stage 03 斑图）
```

---

## 4. SciPy：三个函数撑起半门课

### 4.1 `solve_ivp`：数值解 ODE（讲义 01 的"饭碗"）

三步固定流程：**写右端函数 → 调用 → 取结果**。

```python
import numpy as np
from scipy.integrate import solve_ivp

# 1) 右端函数 f(t, y)，其中 y 是状态向量（哪怕只有一个分量也是数组）
def logistic_rhs(t, y, r, K):
    N = y[0]
    return [r * N * (1 - N / K)]

# 2) 求解：时间区间、初值、参数经 args 传入
sol = solve_ivp(logistic_rhs, t_span=(0, 50), y0=[100.0],
                args=(0.1, 5000.0), t_eval=np.linspace(0, 50, 501),
                rtol=1e-8, atol=1e-8)

# 3) 结果：sol.t 形状 (501,)，sol.y 形状 (1, 501)——注意比 y0 多一层
t, N = sol.t, sol.y[0]
```

三条经验：

- 右端函数签名**必须是 `f(t, y, ...)`**（`t` 在前——历史约定），哪怕方程不显含 $t$；
- `rtol / atol` 调小到 `1e-8`：默认精度对本课程的"解析 vs 数值对照"不够严；
- `t_eval` 让输出落在指定时间点；`dense_output=True` 则提供可任意取值的插值解（练习 ex04 拟合时的关键开关）。

### 4.2 `curve_fit`：数据拟合参数（讲义 03 的 MLE + 讲义 01 的闭环终点）

```python
import numpy as np
from scipy.optimize import curve_fit

# 模型函数：第一个参数必须是自变量，其后是待拟合参数
def logistic_model(t, N0, r, K):
    return K / (1 + (K - N0) / N0 * np.exp(-r * t))

# 伪实验数据：真值 N0=100, r=0.1, K=5000，叠加 5% 噪声
rng = np.random.default_rng(0)
t_data = np.linspace(0, 80, 17)
N_true = logistic_model(t_data, 100.0, 0.1, 5000.0)
N_data = N_true * (1 + rng.normal(0, 0.05, t_data.size))

# 拟合：p0 是初值猜测（curve_fit 是局部优化器，初值很重要！）
p0 = (N_data[0], 0.08, 4 * N_data[-1])
popt, pcov = curve_fit(logistic_model, t_data, N_data, p0=p0)
print("估计值:", popt)                # 应接近 (100, 0.1, 5000)
print("标准误:", np.sqrt(np.diag(pcov)))   # 参数不确定度（一阶近似）
```

注意 `pcov` 给出的是**高斯近似的参数不确定度**——它是讲义 03 第 6.4 节所说"点估计不带不确定度"问题的一阶补丁，Stage 04 会用完整后验分布取代它。

### 4.3 `minimize`：通用数值优化（练习 ex03 的主角）

```python
from scipy.optimize import minimize
from scipy.special import gammaln

def neg_log_likelihood(lam, data):
    # 泊松分布的负对数似然：n*lam - sum(x ln lam) + sum(ln x!)
    n = data.size
    return n * lam - np.sum(data) * np.log(lam) + np.sum(gammaln(data + 1))

result = minimize(neg_log_likelihood, x0=3.0, args=(counts,),
                  bounds=[(1e-9, None)])
lambda_hat = result.x[0]              # 应非常接近 counts.mean()
```

这就是讲义 03 第 6.2 节手推结果的数值版本——**同一个答案，两条路**：解析路告诉你"为什么是均值"，数值路在解析失效时（任意分布、任意约束）依然可行。本仓库的学习标准是两条路都会走。

---

## 5. Jupyter：科学家的实验记录本

### 5.1 为什么是它

Jupyter Notebook 把**推导（Markdown）、代码（Python）、结果（图 / 表）**放进同一个可执行文档——本仓库所有里程碑项目都以 notebook 形式交付（Stage 00 里程碑就是一份 notebook）。

```bash
jupyter lab            # 或旧版界面 jupyter notebook
```

### 5.2 必会操作（10 分钟掌握）

- 单元格两种类型：`Code` 与 `Markdown`（数学公式直接写 `$$...$$`，与讲义同款 LaTeX）；
- `Shift + Enter` 运行当前格并跳到下一格；`Esc` + `M` 把格子转为 Markdown；
- 运行顺序即状态顺序：单元格旁的 `[3]` 表示第 3 个运行——**乱序运行是 notebook 一切"玄学 bug"的根源**，出现怪结果先 `Kernel → Restart & Run All`；
- 魔法命令：`%timeit f(x)`（计时，比大小写两种实现）、`%matplotlib inline`（旧版 Jupyter 需要的绘图内嵌开关）。

### 5.3 工作流约定（本仓库统一）

每个 notebook 顶部三格：**Markdown 格式的标题与问题陈述 → 参数集中在一个"配置格" → 数据加载 / 生成**。改实验只改配置格——这让 notebook 天然可复现，也让 AI 评审时只需贴出配置格与目标函数即可。

---

## 6. 把三讲数学映射到函数调用（速查表）

| 数学（讲义） | Python | 备注 |
|---|---|---|
| $N(t) = N_0 e^{rt}$（讲义 01） | `N0 * np.exp(r * t)` | 向量化，无循环 |
| 欧拉法 $N + f(N)\Delta t$（讲义 01） | 手写 for 循环（练习 ex01） | 理解 `solve_ivp` 在做什么 |
| $\frac{dN}{dt} = f(N)$ 的解 | `solve_ivp(f, t_span, y0, args=...)` | 高阶自适应方法 |
| $A\mathbf{v}$、特征值（讲义 02） | `A @ v`、`np.linalg.eig(A)` | 复数结果取 `.real` / `.imag` |
| $e^{At}$（讲义 02） | `scipy.linalg.expm(A * t) @ x0` | 矩阵指数，非逐元素 `np.exp` |
| 泊松采样 / 直方图（讲义 03） | `rng.poisson(lam, size)`、`ax.hist(...)` | 固定种子保证可复现 |
| MLE / 最小二乘（讲义 03） | `minimize(nll, ...)` / `curve_fit(...)` | 解析 + 数值双路都走 |
| 高斯噪声 | `rng.normal(0, sigma, size)` | 生成伪实验数据 |

> `expm` 注意：`np.exp(A)` 是**逐元素**指数，`scipy.linalg.expm(A)` 才是矩阵指数 $e^{A}$——这是本讲义系列最后一个"写错不报错"陷阱（练习 ex02 中你会同时用到两者，体会区别）。

---

## 7. 本讲小结

- 工具链四件套：**NumPy（算）、Matplotlib（看）、SciPy（解与拟合）、Jupyter（记）**；
- 三条肌肉记忆：向量化优先、轴标签带单位、解析解与数值解同图对照；
- 三个无声陷阱：`*` vs `@`、`np.exp` vs `expm`、`arange` vs `linspace`；
- 闭环工作流 `solve_ivp → 绘图 → curve_fit` 就是 Stage 00 里程碑项目的全部技术内容。

---

## 8. 自测任务（不看书完成）

1. 用一行 NumPy 代码生成 $t \in [0, 10]$（201 点）上 $\frac{dN}{dt} = 0.3N$、$N_0=50$ 的解析解曲线；
2. 用 `solve_ivp` 数值求解上题并计算与解析解的最大相对误差（应 < $10^{-6}$）；
3. 对 `x = np.linspace(0, 5, 6)` 与 `A = np.array([[1,2],[3,4]])`，预测 `A * x[:2]`、`A @ x[:2]`、`np.exp(A)`、`expm(A)` 各是什么形状与内容，再运行验证；
4. 生成 200 个均值为 7 的泊松样本，用 `minimize` 求 MLE，与样本均值之差应 < 0.05。

---

## 9. 配套练习与延伸阅读

- **动手**（按顺序完成）：
  - [ex01-cell-growth.py](../exercises/ex01-cell-growth.py) —— 解析解 + 欧拉法 + `solve_ivp` 三线同图
  - [ex02-matrix-dynamics.py](../exercises/ex02-matrix-dynamics.py) —— 特征值 + `expm` 轨迹
  - [ex03-mle-poission.py](../exercises/ex03-mle-poission.py) —— 手写 NLL + `minimize`
  - [ex04-ode-fit.py](../exercises/ex04-ode-fit.py) —— `solve_ivp` + `curve_fit`（**里程碑项目 `stage00-logistic` 的预演**）
- **延伸**：NumPy 官方《absolute beginner's guide》（前两节即可）；SciPy Cookbook 的 ODE 教程；Matplotlib 官方画廊（找一张喜欢的图读源码）。

→ 完成四个练习后，回到 [Stage 00 README](../README.md) 的里程碑项目一节，组装你的 `stage00-logistic` 完整闭环。
