# grid（棚格检测）路由

## 定位

- 零售棚格单类别 bbox 检测；YOLOv8m、imgsz=800；
- 模型不承担商品分组 / SKU 区分 / 价签归属；
- 当前瓶颈是标注定义/边界规则/困难场景标签不一致，不是训练轮数。

## 事实快照（2026-09-23，当前）

- **沙河批次（0826/0827，TianHong_00123）**：回收 34320 框 → R3 校正 −1 → R15 净删 126 → R8 删 13 → **定稿 1758 图 / 34180 框**；
  按货架类型切分（货架隔离）：立式 288/36/60、阶梯 588/96/108、标准 300/36/60、挂钩 138/30/18（合计 1314/198/246）。
- **mix7 训练集**：7 来源、固定 epoch 14000、来源配额 3000/2280/1920/1440/1680/1680/2000（沙河唯一图 1314，≈1.52× 采样）；
  两个对照：A 从 v2.2.9 起、B 从 mix6 续训。
- **沙河域评测**（4 类型 test + shahe_all 246，口径 conf 0.45 / NMS 0.45 / match IoU 0.5 / imgsz 800）：
  mix7 **0.9418**（比 mix6 +0.0086，立式风幕柜 +0.0357，FN 337→249）> mix6_ft 0.9393 > mix6 0.9332 > v2.2.9 0.9223；
  老域 grid3345 持平（+0.0006）、通用域 grid2000 +0.0012，未见明显遗忘。
- **6 来源测试集重标后**（1122 张，回流清洗标签）：mix6_ft **0.9285** > mix7 0.9261 ≈ mix6 0.9258 > v2.2.9 0.9186；
  **标签清洗使所有模型 F1 整体下降 0.011~0.013** → 历史数字必须标注"旧标签口径"（见 bugs：测试集标签清洗）。
  **该新测试集经业务确认（2026-09-24）与业务判断口径对齐，是当前唯一对外基准**；指标下降属口径修正、非模型退化
  （四模型降幅 −0.0111~−0.0127、极差 0.0016，排名不变）。
- **badcase 归因**：立式风幕柜漏检率最高（10~11%）> 阶梯 4.1~4.4% ≈ 标准 4.1~4.5% > 挂钩 3.2~3.6%；
  mix7 偏保守（FP 少）、mix6_ft 偏激进（FN 少）。
- **测试集维护**：业务确认的 4 张堆头图已从本地与服务器所有 split/清单移除（归档 `<GRID_SERVER_LJH>/_archive_20260923_duitou2/`），
  6 来源测试集 1126→1122、grid2000 168→166。
- **标签版本核定（2026-09-24）**：数据集增加版本标记（`data/datasets/README_LABELS_VERSION.md`、目录内 `LABELS_VERSION.md` /
  `LABELS_VERSION_DEPRECATED.md`）。**最新可用**：沙河 0826/0827 定稿（34180 框，train/val/test 三片都是定稿）、
  6 来源测试集人工再清洗标签（1122，业务基准）、mix7 训练集（train 8733 / val 1023 / test 1122）。
  **遗留**：6 来源目前只有 test 分片做过人工再清洗，train/val 仍为历史版本；1356/636 仍为预标注待回收。
- **当前权重**：
  - 沙河域最优 `<GRID_SERVER_LJH>/runs/mix7_shahe_20260921/runs/v229_mix7_shahe/weights/best.pt`
  - 六来源最优 `<GRID_SERVER_LJH>/runs/mix7_shahe_20260921/runs/mix6_ft_shahe/weights/best.pt`
- **待办**：① 选型拍板（沙河优先 mix7 / 兼顾老域 mix6_ft）② 修选模口径（沙河 198 val 未用，best epoch=4 早停）③ conf 扫描
  ④ 1356（1356 图）+636（636 图）回收后并入 mix8（沙河占比预计 ~35%）。

## 事实快照（2026-09-07，历史；以下条目部分已被取代）

> 保留用于追溯；当前结论请看上一节"事实快照（2026-09-23）"。

- 当时 winner：`<GRID_SERVER_LIUTING>/grid_merged_balanced_20260902/manifest_v2_optuna_trial10/v229_stability_manifestv2_trial10/weights/best.pt`；
  （**已过期**：现沙河域候选为 mix7 / mix6_ft，见上）
- 数据：四来源 merged 7047（3345+1145+852+grid2000(1705)，train/val/test=5593/733/721）；
- 固定五测试集：3345(335) / 1145(132) / 4490(467) / 2000(200) / 6490(667)；
  （仍有效；但沙河批次使用上述新口径，两套口径不可混比）
- 口径：match IoU=0.5；汇报 F1 用 conf=0.45（0.25 只作 badcase 放大镜）；NMS 线上 0.7；
  最优工作点 conf≈0.45~0.50；grid3345 保护线=回退 ≤0.01（详见 `global/训练评测规范.md`）；
  （沙河批次评测用 NMS 0.45，见 `global/训练评测规范.md` 第 5 节说明）
- 候选结论：stability-v2（对方）综合 F1 最高 0.9516；D（我方）综合 mAP 最高 0.884、业务最稳；
  E（我方）新域（1145/852/沙河80）最强；
- 已被否决：v2.2.9 微调路线、纯 1145/4490 重训、A2（均衡 val+F1 早停）、
  manifest v1（6000/epoch 漏图）、NMS=0.45 线上协议、E9（权重损坏未训成）；
- 下一步（当时）：标注规范统一 → 专项数据与评估 → 定向补数 → box/cls/dfl 受控实验 → 结构/分辨率实验。

## 路由

### 业务项目（只读事实，代码在业务侧）

- 本地：`<GRID_ROOT>`（复盘/周报/脚本/可视化都在此，暂非 git 仓）；
- 服务器我方：`<GRID_SERVER_LJH>`；对方/领导侧：`<GRID_SERVER_LIUTING>`（服务器只读）；
- 权威复盘文档：`<GRID_ROOT>\grid_work_review_and_plan_20260907.md`（含服务器核对记录第 5 部分）；
- 压缩上下文：`<GRID_ROOT>\conversation_summary.md`；周报：`weekly_report_20260903.md`；
- 后续规划：`grid_precision_optimization_plan_20260907.md`；
- **2026-09 新增**（沙河批次 / mix7）：
  - 交接文档：`<GRID_ROOT>\HANDOVER_棚格检测迭代_20260923.md`
  - 全流程 + Skill 清单：`<GRID_ROOT>\PROCESS_AND_SKILLS_棚格迭代_20260923.md`
  - 沙河域训练评测报告：`<GRID_ROOT>\mix7_训练与评测报告_20260922.md`
  - 新测试集（回流标签）评测报告：`<GRID_ROOT>\新测试集评测报告_20260923.md`
  - 训练清单标签路径事故复盘：`<GRID_ROOT>\mix7_label_path_incident_20260922.md`
  - 定稿数据上传指引：`<GRID_ROOT>\tianhong0826_0827_上传指引_20260922.md`
  - 清洗规则库：`<GRID_ROOT>\grid_rules_v4_20260915.yaml`；标注任务 SOP：`<GRID_ROOT>\annotation_task_sop_20260915.md`
  - 服务器产物：`<GRID_SERVER_LJH>/runs/mix7_shahe_20260921/eval/`（沙河评测）、
    `<GRID_SERVER_LJH>/runs/testset_clean_20260923/`（新测试集评测 + 新旧标签对比）、
    `<GRID_SERVER_LJH>/runs/badcase_3color_20260923/`（三色 badcase + `index_*.html`）

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

2026-09-23 新增：

- [训练清单用 `Path.resolve()` 导致标签路径解析失败](bugs/manifest_resolve_label_path.md)
- [隔离/移动源文件后标签软链断链，审计看不出来](bugs/broken_symlink_after_isolation.md)
- [测试集标签清洗/换版会让所有模型指标整体变化](bugs/testset_relabel_changes_metrics.md)
- [堆头（促销堆叠陈列）被标成棚格](bugs/duitou_labeled_as_grid.md)
- [训练 val 不含目标域 → best.pt 是按老域选出来的](bugs/train_val_missing_target_domain.md)
