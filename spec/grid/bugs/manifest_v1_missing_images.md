---
tags: [sampling, manifest, grid]
status: 已处置（2026-09）
---

# manifest v1 固定清单漏图

## 现象
每 epoch 固定 6000 条、清单只生成一次、各轮不重抽：非 native 比例永久漏掉部分训练图。

## 根因
配额按来源比例计算但 epoch size 太小，来源配额 < 该来源真实图片数；
清单生成后不再补抽，训练很多 epoch 也见不到漏掉的那部分图。

## 证据
- v1：equal_business/stability 唯一图 4563（漏 1030）；recent_heavy 唯一图 3963（漏 1630）；
- v2：epoch size=10800 后四种配比都覆盖全部 5593 张唯一训练图。

## 处置
- 共同 epoch size = max(ceil(来源训练数/来源比例))；
- 配额≥来源数时整源循环 + 余数无放回抽样；固定 seed；
- 生成后审计：每条 manifest 行数 = epoch size 且唯一图数 = 全量训练图数。

## 预防
- 数据量变化后重新计算 epoch size，不机械沿用 10800；
- 审计脚本纳入训练前检查。
