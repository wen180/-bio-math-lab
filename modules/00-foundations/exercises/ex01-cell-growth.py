# -*- coding: utf-8 -*-
"""
练习 01 · 细胞生长：指数增长与 logistic 模型
=============================================

生物学背景
----------
周一早上，你把 ``N0`` 个细胞接种进培养皿，此后定时计数。

* 培养基近乎无限（对数生长期）：每个细胞以净速率 ``r`` 分裂，
  得微分方程 ``dN/dt = r*N``，解析解为 J 形的指数曲线。
* 营养与空间有限（环境容纳量 ``K``）：拥挤效应按 ``(1 - N/K)`` 给增长踩刹车，
  得 logistic 方程 ``dN/dt = r*N*(1 - N/K)``，解析解为 S 形曲线，拐点在 ``K/2``。

本练习把讲义 01 的全部数学变成代码：解析解、手写欧拉法数值解、
以及 ``scipy.integrate.solve_ivp`` 三条路线放在同一张图上对照。

对应讲义：modules/00-foundations/lectures/01-calculus-for-dynamics.md

任务清单
--------
TODO(1)  实现指数增长解析解 ``exponential_growth``
TODO(2)  实现 logistic 解析解 ``logistic_analytic``
TODO(3)  实现 ODE 右端函数 ``logistic_rhs``（solve_ivp 与欧拉法共用）
TODO(4)  实现通用显式欧拉法 ``euler``
TODO(5)  在主程序的循环里计算欧拉法的最大相对误差
选做(6)  观察底部子图的"数值爆炸演示"，回答文末思考题

运行
----
    python ex01-cell-growth.py

预期结果
--------
* 图 1：指数增长 J 形曲线；
* 图 2（上）：logistic 的解析解 / solve_ivp / 欧拉法三线同图；
* 图 2（下）：步长过大时欧拉法在 K 附近振荡发散的演示；
* 终端打印误差表：步长每减半，最大相对误差约减半（一阶方法，斜率约 1）；
* 全部 assert 通过。

思考题（写进你的 progress.md）
-------------------------------
1. dt=12 时解为什么会在 K 附近上下振荡乃至发散？
   把 r 减半（0.1），要多大的 dt 才会再次触发不稳定？
   （提示：不稳定条件与乘积 r*dt 有关，讲义 01 §6.3。）
2. 若把 K 改成 500（拥挤来得更早），固定 dt=2.0 的欧拉法误差会变大还是变小？
   先预测再运行验证。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# 全局参数（做实验时改这里，不要改函数内部）
# ---------------------------------------------------------------------------
N0 = 100.0     # 初始细胞数
R = 0.2        # 净增长率 r (1/h)
K = 1000.0     # 环境容纳量 K
T_END = 60.0   # 模拟总时长 (h)


# ===========================================================================
# Part 1 · 解析解
# ===========================================================================
def exponential_growth(t, N0, r):
    """指数增长解析解 N(t) = N0 * exp(r*t)。

    Parameters
    ----------
    t : array_like 或 float
        时间点。
    N0, r : float
        初值与净增长率。

    Returns
    -------
    ndarray 或 float
        与 t 同形状的 N(t)。
    """
    # TODO(1): 一行实现（讲义 01 §4.3 已手推过）
    raise NotImplementedError("TODO(1): 实现 exponential_growth")


def logistic_analytic(t, N0, r, K):
    """logistic 增长解析解：

        N(t) = K / (1 + (K - N0)/N0 * exp(-r*t))

    Parameters
    ----------
    t : array_like 或 float
    N0, r, K : float
        初值、增长率、环境容纳量。
    """
    # TODO(2): 按上式实现。自查：t=0 时应返回 N0；t 很大时应返回接近 K
    raise NotImplementedError("TODO(2): 实现 logistic_analytic")


def logistic_rhs(t, y, r, K):
    """ODE 右端 f(t, y)。

    注意 solve_ivp 的约定：状态 y 必须是向量（哪怕只有 1 个分量），
    返回值也必须是列表 / 数组（长度与 y 相同）。

    Parameters
    ----------
    t : float
        时间（本方程不显含 t，但参数必须保留在签名里）。
    y : array_like, shape (1,)
        状态向量，y[0] = N。
    r, K : float
        速率与容量参数。

    Returns
    -------
    list
        长度为 1 的列表 [dN/dt]。
    """
    # TODO(3): 取出 N = y[0]，返回 [logistic 方程右端的值]
    raise NotImplementedError("TODO(3): 实现 logistic_rhs")


# ===========================================================================
# Part 2 · 数值解：显式欧拉法
# ===========================================================================
def euler(f, x0, t, args=()):
    """通用显式欧拉法（标量状态）。

    核心思想（讲义 01 §6.2）：沿当前点的切线走一小步

        x[i] = x[i-1] + f(t[i-1], x[i-1]) * (t[i] - t[i-1])

    Parameters
    ----------
    f : callable
        右端函数，签名 ``f(t, x, *args) -> dx/dt``（返回标量）。
    x0 : float
        初值 x(t[0]) = x0。
    t : ndarray
        递增时间网格（允许不均匀，步长取相邻两点之差）。
    args : tuple
        传给 f 的额外参数。

    Returns
    -------
    ndarray
        与 t 等长的数值解。

    提示
    ----
    * 用 x[i-1] 处的斜率（前向欧拉），不是 x[i] 处的；
    * 循环范围从 1 到 len(t)。
    """
    x = np.empty_like(t, dtype=float)
    x[0] = x0
    # TODO(4): 补全循环体（一到两行）
    raise NotImplementedError("TODO(4): 实现 euler")
    return x


# ===========================================================================
# 主程序（填完 TODO 后无需修改即可运行）
# ===========================================================================
def main():
    t = np.linspace(0.0, T_END, 601)

    # ---------- 图 1：指数增长 ----------
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(t, exponential_growth(t, N0, R), color="tab:red")
    ax1.set_xlabel("time (h)")
    ax1.set_ylabel("cell number N(t)")
    ax1.set_title("Exponential growth: dN/dt = rN")
    fig1.tight_layout()

    # ---------- 图 2：logistic 三线同图 + 数值爆炸演示 ----------
    fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(7, 8))

    # 路线 A：解析解
    N_exact = logistic_analytic(t, N0, R, K)
    # 路线 B：solve_ivp（高阶自适应方法，视为"参考解"）
    sol = solve_ivp(logistic_rhs, (0.0, T_END), [N0],
                    t_eval=t, args=(R, K), rtol=1e-10, atol=1e-10)
    N_scipy = sol.y[0]
    # 路线 C：手写欧拉法（粗步长 dt=2.0，让折线感肉眼可见）
    t_e = np.arange(0.0, T_END + 2.0, 2.0)
    N_euler = euler(logistic_rhs, N0, t_e, args=(R, K))

    ax2.plot(t, N_exact, color="k", lw=2, label="analytic")
    ax2.plot(t, N_scipy, "--", color="tab:blue", lw=1.5, label="solve_ivp")
    ax2.plot(t_e, N_euler, "o-", color="tab:orange", ms=3, label="Euler (dt=2)")
    ax2.axhline(K, color="gray", ls=":", lw=1)
    ax2.text(T_END * 0.02, K * 1.01, "K")
    ax2.set_xlabel("time (h)")
    ax2.set_ylabel("cell number N(t)")
    ax2.set_title("Logistic growth: three solutions on one plot")
    ax2.legend()

    # 自检 1：解析解的边界行为
    assert np.isclose(logistic_analytic(0.0, N0, R, K), N0), \
        "t=0 时解析解应等于 N0（检查你的 TODO(2)）"
    assert abs(N_exact[-1] - K) / K < 1e-3, \
        "t=T_END 时解析解应非常接近 K"

    # 自检 2：solve_ivp 与解析解一致
    err_scipy = np.max(np.abs(N_scipy - N_exact) / N_exact)
    print(f"[自检] solve_ivp vs 解析解 最大相对误差 = {err_scipy:.3e}")
    assert err_scipy < 1e-6, "solve_ivp 与解析解应几乎一致"

    # 自检 3：欧拉法（dt=2）误差量级
    N_euler_on_t = euler(logistic_rhs, N0, t, args=(R, K))
    err_euler = np.max(np.abs(N_euler_on_t - N_exact) / N_exact)
    print(f"[自检] 欧拉法(dt=2) vs 解析解 最大相对误差 = {err_euler:.3e}")
    assert err_euler < 0.05, "dt=2 的欧拉法误差应在 5% 以内"

    # ---------- 误差 - 步长收敛阶 ----------
    print("\n[误差表] 欧拉法最大相对误差随步长收敛（一阶方法：减半→约减半）")
    dt_list = [2.0, 1.0, 0.5, 0.25, 0.125]
    errors = []
    for dt in dt_list:
        t_h = np.arange(0.0, T_END + dt, dt)
        N_h = euler(logistic_rhs, N0, t_h, args=(R, K))
        N_ref = logistic_analytic(t_h, N0, R, K)
        # TODO(5): 计算最大相对误差 err 并 append 到 errors
        #   提示：np.max(np.abs(...)) / N_ref 的组合
        raise NotImplementedError("TODO(5): 计算最大相对误差")
        errors.append(err)
        print(f"  dt = {dt:6.3f}   max_rel_err = {err:.4e}")

    for i in range(len(errors) - 1):
        ratio = errors[i] / errors[i + 1]
        print(f"  dt {dt_list[i]:.3f} -> {dt_list[i + 1]:.3f} : 误差缩小 {ratio:.2f} 倍")
        assert 1.6 < ratio < 2.6, "步长减半误差应约减半（一阶方法）"

    fig3, ax4 = plt.subplots(figsize=(5.5, 4))
    ax4.loglog(dt_list, errors, "o-")
    ax4.set_xlabel("step size dt (h)")
    ax4.set_ylabel("max relative error")
    ax4.set_title("Euler method: first-order convergence")

    # ---------- 选做：数值稳定性演示 ----------
    # r * dt = 0.2 * 12 = 2.4 > 2，违反显式欧拉在 N≈K 附近的稳定性条件
    t_blow = np.arange(0.0, 300.0, 12.0)
    N_blow = euler(logistic_rhs, N0, t_blow, args=(R, K))
    ax3.plot(t_blow, N_blow, "o-", color="tab:red")
    ax3.axhline(K, color="gray", ls=":", lw=1)
    ax3.set_xlabel("time (h)")
    ax3.set_ylabel("cell number N(t)")
    ax3.set_title("Numerical instability: Euler with r*dt = 2.4 > 2")

    fig2.tight_layout()
    plt.show()
    print("\n全部自检通过 ✅  记得把思考题的答案写进 progress.md")


if __name__ == "__main__":
    main()
