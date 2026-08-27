# -*- coding: utf-8 -*-
"""
练习 03 · 泊松分布 mRNA 计数的极大似然估计（MLE）
=================================================

生物学背景
----------
用单分子 FISH（smFISH）测量某基因在单细胞中的 mRNA 拷贝数：
每个细胞数出亮点的个数，得到一批计数数据（非负整数）。

若该基因以恒定速率、独立地转录（启动子常开、无突发），
稳态拷贝数近似服从泊松分布 Poisson(lambda)——其中 lambda 既是均值也是方差。

本练习走讲义 03 §6.2 手推结果的**数值路线**：

    手写负对数似然 NLL(lambda) → scipy.optimize.minimize 数值最小化
    → 与解析答案（样本均值）对照

两条路必须都会走：解析路给洞察，数值路在换任何分布后依然可行
（Stage 04 的全部拟合都要走数值路）。

对应讲义：modules/00-foundations/lectures/03-probability-statistics.md

任务清单
--------
TODO(1)  实现负对数似然 ``neg_log_likelihood``
TODO(2)  在主程序中调用 ``minimize`` 完成 MLE
TODO(3)  在主程序中计算样本均值、样本方差与 Fano factor 并打印
选做(4)  把 LAMBDA_TRUE 改成 1.0（更低拷贝）重跑：
         直方图更偏斜，Fano 因采样涨落波动更大——先预测再验证

运行
----
    python ex03-mle-poission.py

预期结果
--------
* MLE 估计值 lambda_hat 与样本均值几乎一致（相对差 < 1e-3）；
* 图 1（上）：计数直方图 + 拟合泊松 PMF（lambda_hat）+ 真值 PMF（虚线）；
* 图 1（下）：NLL(lambda) 曲线（似然"山谷"），最低点与 lambda_hat、样本均值
  三点应重合；
* 全部 assert 通过。

思考题（写进你的 progress.md）
-------------------------------
1. 本练习里 MLE 恰好等于样本均值。对泊松分布这是解析可证的（讲义 03 §6.2）。
   换成指数分布（等待时间数据），MLE 是样本均值还是别的？试着只改
   neg_log_likelihood 一处函数体，验证你的猜想。
2. 若真实数据来自"突发转录"（两态启动子），Fano factor 通常 >> 1。
   此时仍用泊松 MLE 会发生什么？MLE 会"错"在哪里——优化失败，还是
   模型选错了？（后者。这正是 Stage 04 模型比较的动机。）
3. 把 N_CELLS 从 300 改成 30：lambda_hat 波动多大？这如何量化成
   "参数不确定度"？（Stage 04 的后验分布将给出完整答案。）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.special import gammaln

# ---------------------------------------------------------------------------
# 全局参数（做实验时改这里）
# ---------------------------------------------------------------------------
LAMBDA_TRUE = 3.5   # 真实平均 mRNA 拷贝数 / 细胞
N_CELLS = 300       # 测量的细胞数
SEED = 2026         # 随机种子（固定以保证可复现）


# ===========================================================================
# Part 1 · 负对数似然
# ===========================================================================
def neg_log_likelihood(lam, data):
    """泊松分布的负对数似然（NLL）。

    对 i.i.d. 观测 data = (x_1, ..., x_n)，泊松对数似然为

        l(lam) = sum_i [ -lam + x_i * ln(lam) - ln(x_i!) ]

    于是

        NLL(lam) = n*lam - (sum_i x_i) * ln(lam) + sum_i ln(x_i!)

    Parameters
    ----------
    lam : float
        泊松参数（> 0）。minimize 会以长度 1 的数组传入。
    data : ndarray
        非负整数计数。

    Returns
    -------
    float

    提示
    ----
    * lam 可能是长度 1 的数组：用 float(lam) 或 lam 取第 0 个元素；
    * ln(x!) 请用 gammaln(x + 1)（scipy.special），不要用 np.math.factorial
      （大数阶乘会溢出，且浮点数不支持）；
    * 常数项 sum ln(x_i!) 不影响最小化位置，但建议保留——
      这样 NLL 数值可与手算对照。
    """
    # TODO(1): 按上式实现并返回 NLL
    raise NotImplementedError("TODO(1): 实现 neg_log_likelihood")


# ===========================================================================
# 主程序（填完 TODO 后无需修改即可运行）
# ===========================================================================
def main():
    # ---------- 生成模拟数据（视为 smFISH 计数） ----------
    rng = np.random.default_rng(SEED)
    counts = rng.poisson(lam=LAMBDA_TRUE, size=N_CELLS)

    # TODO(3): 计算并打印三个统计量（提示：counts.mean() / counts.var()）
    #   * sample_mean  样本均值
    #   * sample_var   样本方差
    #   * fano         = sample_var / sample_mean
    raise NotImplementedError("TODO(3): 计算样本统计量与 Fano factor")
    print(f"模拟数据：n = {N_CELLS} 个细胞，lambda_true = {LAMBDA_TRUE}")
    print(f"样本均值 = {sample_mean:.4f}")
    print(f"样本方差 = {sample_var:.4f}")
    print(f"Fano factor (var/mean) = {fano:.4f}   （泊松理论值 = 1）")
    assert 0.5 < fano < 1.5, "泊松数据的 Fano 应接近 1（采样涨落范围内）"

    # ---------- 数值 MLE ----------
    # TODO(2): 调用 minimize 求解：
    #   * 目标函数：neg_log_likelihood
    #   * 初值 x0：取一个粗略猜测（例如 5.0；不用太准）
    #   * args：传 (counts,)
    #   * bounds：[(1e-9, None)] 保证 lam > 0（NLL 在 lam->0+ 时发散）
    #   结果取 res.x[0] 作为 lambda_hat
    raise NotImplementedError("TODO(2): 调用 minimize 完成 MLE")
    lambda_hat = res.x[0]

    print(f"\n数值 MLE:  lambda_hat = {lambda_hat:.6f}")
    print(f"解析 MLE:  样本均值    = {sample_mean:.6f}")
    rel_diff = abs(lambda_hat - sample_mean) / sample_mean
    print(f"两者相对差 = {rel_diff:.2e}")
    assert rel_diff < 1e-3, "数值 MLE 应与解析答案（样本均值）一致"

    # ---------- NLL 山谷与拟合质量 ----------
    lam_grid = np.linspace(1.5, 6.5, 301)
    nll_grid = np.array([neg_log_likelihood(l, counts) for l in lam_grid])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8))

    bins = np.arange(-0.5, counts.max() + 1.5, 1.0)
    ax1.hist(counts, bins=bins, density=True, color="tab:blue",
             alpha=0.6, label="simulated counts")
    k = np.arange(0, counts.max() + 2)
    pmf_fit = np.exp(-lambda_hat + k * np.log(lambda_hat) - gammaln(k + 1))
    pmf_true = np.exp(-LAMBDA_TRUE + k * np.log(LAMBDA_TRUE) - gammaln(k + 1))
    ax1.plot(k, pmf_fit, "o-", color="tab:red", label=f"fit PMF ($\\lambda$={lambda_hat:.2f})")
    ax1.plot(k, pmf_true, "s--", color="k", ms=4,
             label=f"true PMF ($\\lambda$={LAMBDA_TRUE})")
    ax1.set_xlabel("mRNA copies per cell")
    ax1.set_ylabel("probability")
    ax1.set_title("smFISH-style counts: data vs fitted Poisson")
    ax1.legend()

    ax2.plot(lam_grid, nll_grid, color="tab:blue")
    ax2.axvline(lambda_hat, color="tab:red", ls="--",
                label=f"numerical MLE = {lambda_hat:.3f}")
    ax2.axvline(sample_mean, color="tab:green", ls=":",
                label=f"sample mean = {sample_mean:.3f}")
    ax2.axvline(LAMBDA_TRUE, color="gray", ls="-.", lw=1,
                label=f"true $\\lambda$ = {LAMBDA_TRUE}")
    ax2.set_xlabel("lambda")
    ax2.set_ylabel("negative log-likelihood")
    ax2.set_title("Likelihood valley: NLL(lambda)")
    ax2.legend()

    fig.tight_layout()
    plt.show()
    print("\n全部自检通过 ✅  思考题 2 是 Stage 04 模型比较的第一颗种子")


if __name__ == "__main__":
    main()
