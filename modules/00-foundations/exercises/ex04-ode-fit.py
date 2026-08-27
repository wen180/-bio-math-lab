# -*- coding: utf-8 -*-
"""
练习 04 · 从数据反推参数：logistic 拟合（里程碑项目预演）
=========================================================

生物学背景
----------
你面对一组"实验数据"：某培养皿在 17 个时间点的细胞计数，
每个测量值带约 5% 的乘性噪声（模拟血球计数板 / OD600 的测量误差）。
你知道增长服从 logistic 动力学，但参数 (N0, r, K) 未知。

任务：从噪声数据恢复这三个参数——这正是科学实践中"反问题"的最小样本：
**模型结构已知（来自 Stage 01 之前的机理推导），参数未知（来自数据）。**

本练习是 Stage 00 里程碑项目 `stage00-logistic` 的直接预演：
跑通它之后，把同样的工作流（生成数据 → 包装模型 → curve_fit → 对照真值）
原封不动搬进你的里程碑 notebook 即可。

对应讲义：modules/00-foundations/lectures/04-python-scientific-stack.md §4.2
（噪声模型与 MLE 的关系见讲义 03 §6.3：高斯噪声下 curve_fit 的最小二乘
目标函数 = 极大似然。）

任务清单
--------
TODO(1)  实现 ODE 右端 ``logistic_rhs``（与 ex01 相同——温故）
TODO(2)  实现"把 solve_ivp 包装成 curve_fit 可用模型"的 ``logistic_model``
TODO(3)  在主程序中调用 ``curve_fit`` 完成拟合（含初值 p0）
TODO(4)  计算三个参数的相对误差并打印（要求全部 < 10%）
选做(5)  参数不确定度：用 pcov 计算各参数的一倍标准误并打印，
         与"真值是否落在 ±1σ 内"对照（Stage 04 后验分布的一阶预览）

运行
----
    python ex04-ode-fit.py

预期结果
--------
* 终端打印参数对照表：估计值 vs 真值，相对误差全部 < 10%；
* 图 1：噪声数据点 + 拟合曲线 + 真值曲线，三者同图；
* 全部 assert 通过。

思考题（写进你的 progress.md）
-------------------------------
1. 把 T_END 从 80 改成 30（数据没有跨越拐点 K/2 ≈ 2500，发生在 t ≈ 39h）：
   K 的相对误差会怎么变？r 呢？先预测再运行。——这正是里程碑项目
   反思题的数值版："采样范围是否覆盖了足以约束参数的动力学阶段？"
2. 把 NOISE_STD 改成 0.15（噪声增大 3 倍）：哪些参数先失去精度？
   重复运行几次（改 SEED）观察估计值的波动——这个波动就是
   "参数不确定度"的 bootstrap 直觉。
3. curve_fit 拟合的是"乘性高斯噪声"的模型吗？严格说它最小化的是
   加性残差平方和。对计数数据（泊松噪声）应该改用什么目标函数？
   （讲义 03 §6.3。）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# 全局参数
# ---------------------------------------------------------------------------
N0_TRUE = 100.0    # 真值：初始细胞数
R_TRUE = 0.1       # 真值：净增长率 (1/h)
K_TRUE = 5000.0    # 真值：环境容纳量
T_END = 80.0       # 采样总时长 (h)
N_POINTS = 17      # 采样点数
NOISE_STD = 0.05   # 乘性测量噪声（标准差 / 信号）
SEED = 7           # 随机种子


# ===========================================================================
# Part 1 · 模型
# ===========================================================================
def logistic_rhs(t, y, r, K):
    """ODE 右端（与 ex01 相同）：y[0] = N。

    注意：t 必须保留在签名里（solve_ivp 的约定），虽然方程不显含 t。
    """
    # TODO(1): 返回 [logistic 方程右端]
    raise NotImplementedError("TODO(1): 实现 logistic_rhs")


def logistic_model(t, N0, r, K):
    """把 solve_ivp 包装成 curve_fit 可用的模型函数。

    curve_fit 的约定：
    * 第一个参数是自变量 t（数组）；
    * 其后依次是待拟合参数（这里：N0, r, K）；
    * 返回与 t 同长度的模型预测值数组。

    实现要点
    --------
    * 每次调用都要做一次全新的积分：t_span = (t[0], t[-1])，
      y0 = [N0]，args = (r, K)，并开启 dense_output=True；
    * 用 sol.sol(t)[0] 在任意时间点取值（t 不必是积分网格）；
    * 假设 t 单调递增（本练习的采样方案满足）。
    """
    # TODO(2): 按"实现要点"写完这个函数
    raise NotImplementedError("TODO(2): 实现 logistic_model")


# ===========================================================================
# Part 2 · 生成伪实验数据（无需修改）
# ===========================================================================
def make_data():
    """用真值生成带噪声的"实验数据"（可复现）。"""
    t_data = np.linspace(0.0, T_END, N_POINTS)
    sol = solve_ivp(logistic_rhs, (0.0, T_END), [N0_TRUE],
                    args=(R_TRUE, K_TRUE), dense_output=True,
                    rtol=1e-10, atol=1e-10)
    N_clean = sol.sol(t_data)[0]
    rng = np.random.default_rng(SEED)
    N_data = N_clean * (1.0 + rng.normal(0.0, NOISE_STD, t_data.size))
    return t_data, N_data


# ===========================================================================
# 主程序（填完 TODO 后无需修改即可运行）
# ===========================================================================
def main():
    t_data, N_data = make_data()

    # TODO(3): 调用 curve_fit：
    #   * 模型函数：logistic_model
    #   * 初值 p0：粗略猜测即可。建议
    #       N0 ≈ 数据第一个点的值；r ≈ 0.08；K ≈ 2 倍的最后一个数据点
    #     （curve_fit 是局部优化器：初值太离谱会收敛到坏极小值）
    #   * 返回 popt（最优参数）与 pcov（参数协方差）
    raise NotImplementedError("TODO(3): 调用 curve_fit")

    N0_fit, r_fit, K_fit = popt

    # TODO(4): 计算三个参数的相对误差（|估计 - 真值| / 真值），
    #   打印一张"参数 / 真值 / 估计值 / 相对误差"对照表
    raise NotImplementedError("TODO(4): 计算并打印相对误差对照表")

    # ---------- 自检 ----------
    assert err_N0 < 0.10, "N0 的相对误差应 < 10%"
    assert err_r < 0.10, "r 的相对误差应 < 10%"
    assert err_K < 0.10, "K 的相对误差应 < 10%"

    # 选做(5)：一倍标准误 = np.sqrt(np.diag(pcov))，
    # 检查真值是否落在 估计值 ± 1σ 之内，并打印结论

    # ---------- 可视化 ----------
    t_fine = np.linspace(0.0, T_END, 400)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(t_data, N_data, s=25, color="k", zorder=3, label="noisy data")
    ax.plot(t_fine, logistic_model(t_fine, N0_fit, r_fit, K_fit),
            color="tab:red", lw=2, label="curve_fit best fit")
    ax.plot(t_fine, logistic_model(t_fine, N0_TRUE, R_TRUE, K_TRUE),
            "--", color="tab:blue", lw=1.5, label="true curve")
    ax.axhline(K_TRUE, color="gray", ls=":", lw=1)
    ax.set_xlabel("time (h)")
    ax.set_ylabel("cell number N(t)")
    ax.set_title("Parameter recovery from noisy logistic data")
    ax.legend()
    fig.tight_layout()
    plt.show()
    print("\n全部自检通过 ✅  下一步：把本练习的工作流搬进里程碑项目 notebook")


if __name__ == "__main__":
    main()
