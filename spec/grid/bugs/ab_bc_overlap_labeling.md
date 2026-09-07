---
tags: [label, overlap, grid]
status: 已处置（2026-09）
---

# AB+BC 同行侵占 / 双框嵌套

## 现象
同一货架层出现"两框盖三格"式重叠：相邻标注框互相侵占（AB+BC），或一个框被另一个完全/部分嵌套。

## 根因
标注者对同层物理边界的判断不一致；跨来源标注标准漂移（1145/852/3345 各自历史）。

## 证据
- clean_grid_1145_3345.py 的 overlap-scan / row-overlap-scan 输出；
- 9 张走排除清单 `excluded_overlap_stems_20260902.txt`，10 张备份 `removed_20260902_backup`；
- preprocess 流水线对 IoU>0.25 连通分量做几何切分（保留独有+相交区域，非 NMS）。

## 处置
- 脚本全量清洗：几何切分 + 同行水平侵占检查；
- 判定为问题的图先排除/备份，不直接删；
- 服务器工具链 `det/tools/preprocess_grid_dataset.py` 落地"切分→补框→二次切分"顺序。

## 预防
- 标注手册明确"同层相邻边界"规则（y/x gap 阈值）；
- 新增批次自动跑 overlap-scan，阈值 IoU>0.25；
- 训练/切分前按排除清单过滤。
