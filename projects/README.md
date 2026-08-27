# 🧪 里程碑项目（projects/）

每个 Stage 结束时，完成一个里程碑项目放这里：**能跑的代码 + 一页纸报告**。这是六个阶段的学习产出，也是未来作品集的主体。

## 命名规范

`stageNN-主题/`，对应六阶段：

| 目录 | 阶段 | 项目内容 |
|---|---|---|
| `stage00-logistic/` | Stage 00 | 细胞生长模型闭环：解析解 + 数值解 + 数据拟合 |
| `stage01-dynamics/` | Stage 01 | toggle switch 双稳态 + repressilator 振荡条件 |
| `stage02-noise/` | Stage 02 | Gillespie SSA 实现 + 基因表达噪声分析 |
| `stage03-pattern/` | Stage 03 | 图灵斑图模拟 + 参数相图 |
| `stage04-inference/` | Stage 04 | 贝叶斯方法从数据恢复 ODE 参数 |
| `stage05-pinn/` | Stage 05 | PINN 求解反应扩散方程 vs 有限差分 |

## 目录内结构（约定）

```text
stage00-logistic/
├── README.md      # 报告：问题 / 方法 / 结果 / 一句话结论
├── main.py        # 主脚本，理想情况一条命令复现全部结果
├── data/          # 数据或数据生成脚本
└── figures/       # 生成的图（由脚本输出，不手改）
```

## 项目三要求

1. **数据可复现**：固定随机种子；README 写清环境（Python 版本 + 关键库版本）与运行命令；图形由脚本生成而非手工绘制。
2. **结论一句话**：报告末尾必须有一句话结论，例如"Euler 法在相同步长下误差比 RK45 高约 3 个数量级"。
3. **第一责任人检验**：报告中注明哪些推导 / 代码经过 AI 辅助；验收标准是能不看材料口头讲清每一行代码的作用。

## 完成定义（DoD）

- [ ] 代码跑通，图与数据可一键复现
- [ ] 一句话结论写入项目 README
- [ ] 能不看材料向别人讲 10 分钟
- [ ] 在 [progress.md](../progress.md) 记录里程碑条目（含掌握度自评）
