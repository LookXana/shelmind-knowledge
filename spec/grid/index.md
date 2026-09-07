# grid（棚格检测）路由

## 定位

- 零售棚格单类别 bbox 检测；YOLOv8m、imgsz=800；
- 模型不承担商品分组 / SKU 区分 / 价签归属；
- 当前瓶颈是标注定义/边界规则/困难场景标签不一致，不是训练轮数。

## 事实快照（2026-09-07）

- 当前 winner：`<GRID_SERVER_LIUTING>/grid_merged_balanced_20260902/manifest_v2_optuna_trial10/v229_stability_manifestv2_trial10/weights/best.pt`；
- 数据：四来源 merged 7047（3345+1145+852+grid2000(1705)，train/val/test=5593/733/721）；
- 固定五测试集：3345(335) / 1145(132) / 4490(467) / 2000(200) / 6490(667)；
- 口径：match IoU=0.5；汇报 F1 用 conf=0.45（0.25 只作 badcase 放大镜）；NMS 线上 0.7；
  最优工作点 conf≈0.45~0.50；grid3345 保护线=回退 ≤0.01（详见 `global/训练评测规范.md`）；
- 候选结论：stability-v2（对方）综合 F1 最高 0.9516；D（我方）综合 mAP 最高 0.884、业务最稳；
  E（我方）新域（1145/852/沙河80）最强；
- 已被否决：v2.2.9 微调路线、纯 1145/4490 重训、A2（均衡 val+F1 早停）、
  manifest v1（6000/epoch 漏图）、NMS=0.45 线上协议、E9（权重损坏未训成）；
- 下一步：标注规范统一 → 专项数据与评估 → 定向补数 → box/cls/dfl 受控实验 → 结构/分辨率实验。

## 路由

### 业务项目（只读事实，代码在业务侧）

- 本地：`<GRID_ROOT>`（复盘/周报/脚本/可视化都在此，暂非 git 仓）；
- 服务器我方：`<GRID_SERVER_LJH>`；对方/领导侧：`<GRID_SERVER_LIUTING>`（服务器只读）；
- 权威复盘文档：`<GRID_ROOT>\grid_work_review_and_plan_20260907.md`（含服务器核对记录第 5 部分）；
- 压缩上下文：`<GRID_ROOT>\conversation_summary.md`；周报：`weekly_report_20260903.md`；
- 后续规划：`grid_precision_optimization_plan_20260907.md`。

### 本仓

- 跨任务口径：`global/训练评测规范.md`；
- 坑点：`bugs/`（列表见下）；
- 训练白名单：`workflows/grid_train.yaml`。

## bugs 索引

- [AB+BC 同行侵占/双框嵌套](bugs/ab_bc_overlap_labeling.md)
- [边缘框阈值随分辨率漂移](bugs/edge_box_standard_drift.md)
- [重复图跨 split 泄漏](bugs/test_leakage_dup_split.md)
- [conf/NMS 口径混用导致误判](bugs/conf_mixup_metrics.md)
- [评测目录复用导致标签累积](bugs/eval_dir_reuse_e8.md)
- [Ultralytics .cache 并发竞争](bugs/ultralytics_cache_race.md)
- [manifest v1 固定清单漏图](bugs/manifest_v1_missing_images.md)
- [预训练权重损坏导致启动崩溃](bugs/corrupted_pretrained_weight_e9.md)
