---
tags: [training, val, model-selection, grid]
status: 待处置（2026-09-23）
---

# 训练 val 不含目标域 → best.pt 是按老域选出来的

## 现象
mix7 两个实验都在 **epoch 4** 就达到 val 最优，随后 patience 25 触发、**epoch 29 早停**
（配置是 120 epoch）。事后核对发现：训练 val（`val_all7.txt` 1024 张）**全部是老域/通用域，没有一张沙河图**；
而沙河域的 198 张 val 从头到尾没被用上（不进训练、不进 val、也不是 test）。

## 根因
数据集装配时 6 来源沿用了 mix6 的 val/test 分片，新批只把 **train 分片**接进来（1314 张），
新批的 val 分片（198 张）落在流程之外 → 选模完全由老域决定。

## 证据
- `manifests/val_all7.txt` 中 `tianhong0826` 命中 0；
- 两个实验 `results.csv`：best epoch = 4（mAP50-95 0.8924/0.8924），epoch 29 停止；
- 沙河域评测 mix7 仍优于 mix6（+0.0086），说明"选错 epoch"没有致命影响，
  但无法确认"沙河最优 epoch"是否被错过。

## 处置
- 下一轮训练把新批 val 分片接进 val 清单（`val_all7_plus_<newbatch>.txt`），重训对照；
- 同时保留老域 val 作为保护线指标（避免为沙河牺牲老域）；
- 早停 patience 结合"目标域 val"重新设定，避免 4 epoch 就触顶。

## 预防
- 数据集装配门禁增加一项：**val 必须覆盖目标域**（按来源/店/货架类型统计 val 覆盖度）；
- 每次回流数据切出的 val 分片必须显式进入 val 或 test，不允许"悬空"；
- 复盘时核对"best epoch 是否过早/过晚"，异常早停要查选模集。
