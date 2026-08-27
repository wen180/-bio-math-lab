# -*- coding: utf-8 -*-
"""
练习 02 · 两状态基因开关的线性动力学
====================================

生物学背景
----------
考虑一个线性化的负反馈基因开关（讲义 02 §1 与 §7）。
两个状态量——mRNA 浓度 x1 与蛋白浓度 x2——互为因果地纠缠：

    dx1/dt = -gamma_M * x1  -  beta  * x2      # mRNA 降解；蛋白抑制转录（负反馈）
    dx2/dt =  alpha  * x1   -  gamma_P * x2    # 翻译产生蛋白；蛋白降解

写成矩阵形式 dx/dt = A @ x，其中

    A = [[-gamma_M, -beta  ],
         [ alpha,   -gamma_P]]

参数（单位 1/h）：gamma_M = 1.0, gamma_P = 0.5, alpha = 2.0, beta = 1.0。

这个"两步负反馈级联"是转录网络中最常见的基序之一（Alon 书第 3 章）：

* 全部特征值实部 < 0  → 扰动被耗散，系统回到稳态；
* 特征值为复数       → 回稳途中先过冲、再阻尼回落（oscillation）；
* 若实部 > 0          → 失稳（本参数下不会发生——但值得想想何时会发生）。

对应讲义：modules/00-foundations/lectures/02-linear-algebra.md

任务清单
--------
TODO(1)  构建系统矩阵 ``build_matrix``
TODO(2)  计算特征值并完成稳定性判断 ``analyze_stability``
TODO(3)  用矩阵指数实现求解器 ``solve_with_expm``：x(t) = expm(A*t) @ x0
TODO(4)  实现迹-行列式快速分类 ``classify_by_trace_det``
选做(5)  把模块级参数 ALPHA 改为 0.2 重跑：特征值应变成两个负实数
         （过阻尼），轨迹不再绕圈——先预测再验证

运行
----
    python ex02-matrix-dynamics.py

预期结果
--------
* 特征值 = -0.75 ± 1.39i（复数、实部为负 → 稳定螺旋：阻尼振荡回稳态）；
* 图 1：x1(t)、x2(t) 阻尼振荡（expm 与 solve_ivp 两条线应重合）；
* 图 2：相平面轨迹从初值 (2, 0) 出发螺旋吸向原点；
* 终端打印迹、行列式与分类结果，全部 assert 通过。

思考题（写进你的 progress.md）
-------------------------------
1. 为什么负反馈的两步级联容易"先过冲再回落"？
   什么样的矩阵结构会给出单调回稳（无过冲）？（选做 5 是一个答案。）
2. 把 BETA 增大到 5（反馈更强）：特征值实部变了吗？虚部呢？
   振荡变快还是变慢？阻尼变强还是变弱？先算 tr 与 det 再运行验证。
3. 这个线性模型对真实基因开关做了哪些近似？
   （提示：Hill 非线性、表达饱和、mRNA 的离散性——分别连接 Stage 01 与 Stage 02。）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.linalg import expm

# ---------------------------------------------------------------------------
# 全局参数（做实验时改这里）
# ---------------------------------------------------------------------------
GAMMA_M = 1.0   # mRNA 降解率 (1/h)
GAMMA_P = 0.5   # 蛋白降解率 (1/h)
ALPHA = 2.0     # 翻译速率系数 (1/h)
BETA = 1.0      # 蛋白对 mRNA 的抑制强度 (1/h)

X0 = np.array([2.0, 0.0])   # 初值：mRNA 偏高、蛋白尚在 0
T_END = 12.0                # 模拟时长 (h)


# ===========================================================================
# Part 1 · 系统矩阵
# ===========================================================================
def build_matrix(gamma_m, gamma_p, alpha, beta):
    """返回线性化基因开关的系统矩阵 A（2x2）。

    结构（行 = 接收方，列 = 发出方；见讲义 02 §3.1）：

        A = [[-gamma_M, -beta  ],
             [ alpha,   -gamma_P]]

    Returns
    -------
    ndarray, shape (2, 2)
    """
    # TODO(1): 用 np.array([[...], [...]]) 构建 A 并返回
    raise NotImplementedError("TODO(1): 实现 build_matrix")


# ===========================================================================
# Part 2 · 特征值与稳定性
# ===========================================================================
def analyze_stability(A, tol=1e-9):
    """计算特征值并判断稳定性与振荡性。

    Parameters
    ----------
    A : ndarray (2, 2)
    tol : float
        判"实部为负 / 虚部为零"的数值容差。

    Returns
    -------
    eigvals : ndarray (2,)
        特征值（可能是复数）。
    is_stable : bool
        所有特征值实部 < -tol。
    is_oscillatory : bool
        任一特征值虚部绝对值 > tol。

    提示
    ----
    eigvals, _ = np.linalg.eig(A) 之后，eigvals.real / eigvals.imag 可用。
    """
    # TODO(2): 计算并返回三个量
    raise NotImplementedError("TODO(2): 实现 analyze_stability")
    # return eigvals, is_stable, is_oscillatory


def classify_by_trace_det(A):
    """用迹-行列式判据给原点分类（讲义 02 §4.4）。

    Returns
    -------
    str : 'stable' | 'unstable' | 'saddle'

    判据
    ----
    det < 0            -> 'saddle'
    tr < 0 且 det > 0  -> 'stable'
    tr > 0 且 det > 0  -> 'unstable'
    """
    # TODO(4): tr = np.trace(A), det = np.linalg.det(A)，按上表返回字符串
    raise NotImplementedError("TODO(4): 实现 classify_by_trace_det")


# ===========================================================================
# Part 3 · 矩阵指数求解
# ===========================================================================
def solve_with_expm(A, x0, t):
    """用矩阵指数求解线性系统 x(t) = expm(A*t) @ x0。

    Parameters
    ----------
    A : ndarray (2, 2)
    x0 : ndarray (2,)
    t : ndarray (n,)
        时间网格。

    Returns
    -------
    X : ndarray (n, 2)
        第 i 行是时刻 t[i] 的状态（行向量）。

    注意
    ----
    * 矩阵指数是 scipy.linalg.expm(A * ti)，**不是** np.exp（逐元素）！
    * 矩阵乘向量用 @。
    """
    X = np.empty((len(t), len(x0)))
    for i, ti in enumerate(t):
        # TODO(3): X[i] = ...
        raise NotImplementedError("TODO(3): 实现 solve_with_expm")
    return X


# ===========================================================================
# 主程序（填完 TODO 后无需修改即可运行）
# ===========================================================================
def main():
    A = build_matrix(GAMMA_M, GAMMA_P, ALPHA, BETA)
    print("系统矩阵 A =")
    print(A)

    eigvals, is_stable, is_osc = analyze_stability(A)
    print(f"\n特征值 = {eigvals}")
    print(f"实部 = {eigvals.real}，虚部 = {eigvals.imag}")
    print(f"稳定？ {is_stable}；振荡？ {is_osc}")

    label = classify_by_trace_det(A)
    print(f"迹 = {np.trace(A):.3f}，行列式 = {np.linalg.det(A):.3f}，"
          f"迹-行列式分类 = '{label}'")

    # ---------- 自检 ----------
    assert is_stable, "本参数组下系统应是稳定的（否则检查矩阵符号）"
    assert is_osc, "本参数组下特征值应为复数（稳定螺旋）"
    assert np.allclose(eigvals.real, -0.75, atol=1e-9), \
        "实部应为 -tr/2 = -0.75"
    assert np.isclose(np.max(np.abs(eigvals.imag)), np.sqrt(7.75) / 2, atol=1e-6), \
        "虚部应为 sqrt(7.75)/2 ≈ 1.3919"
    assert label == "stable", "迹-行列式分类应与特征值符号一致"

    # ---------- 数值求解与对照 ----------
    t = np.linspace(0.0, T_END, 481)
    X = solve_with_expm(A, X0, t)
    sol = solve_ivp(lambda t, x: A @ x, (0.0, T_END), X0,
                    t_eval=t, rtol=1e-10, atol=1e-10)

    err = np.max(np.abs(X - sol.y.T))
    print(f"\n[自检] expm 解与 solve_ivp 解最大绝对误差 = {err:.3e}")
    assert err < 1e-6, "expm 与 solve_ivp 应几乎一致（检查 TODO(3)）"

    # ---------- 图 1：时间轨迹 ----------
    fig1, ax1 = plt.subplots(figsize=(7, 4.5))
    ax1.plot(t, X[:, 0], color="tab:blue", label="mRNA  x1(t)")
    ax1.plot(t, X[:, 1], color="tab:orange", label="protein  x2(t)")
    ax1.plot(sol.t, sol.y[0], "k--", lw=0.8, label="solve_ivp (mRNA)")
    ax1.plot(sol.t, sol.y[1], "k:", lw=0.8, label="solve_ivp (protein)")
    ax1.axhline(0.0, color="gray", lw=0.5)
    ax1.set_xlabel("time (h)")
    ax1.set_ylabel("concentration (a.u.)")
    ax1.set_title("Two-state gene switch: damped oscillation back to steady state")
    ax1.legend(ncol=2)

    # ---------- 图 2：相平面轨迹 ----------
    fig2, ax2 = plt.subplots(figsize=(5.5, 5))
    ax2.plot(X[:, 0], X[:, 1], color="tab:green", label="trajectory")
    ax2.plot(X[0, 0], X[0, 1], "ko", ms=8, label="start (x0)")
    ax2.plot(0, 0, "r*", ms=14, label="fixed point (0,0)")
    ax2.set_xlabel("mRNA  x1")
    ax2.set_ylabel("protein  x2")
    ax2.set_title("Phase portrait: stable spiral")
    ax2.set_aspect("equal")
    ax2.legend()

    fig1.tight_layout()
    fig2.tight_layout()
    plt.show()
    print("\n全部自检通过 ✅  选做(5)：把 ALPHA 改为 0.2 重跑，"
          "观察特征值变为两个负实数、轨迹不再绕圈")


if __name__ == "__main__":
    main()
