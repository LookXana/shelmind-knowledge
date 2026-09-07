---
tags: [eval, conf, nms, grid]
status: 已处置（2026-08/09，需长期遵守）
---

# conf/NMS 口径混用导致误判

## 现象
- val 默认 conf=0.001 导出 3 倍于 GT 的框，badcase 全失真；
- 0.25 的 F1 与 0.45 的 F1 被直接比较；
- NMS IoU 0.45 vs 0.7 的 mAP 被直接比较；
- 早期脚本里 match IoU 默认 0.25、报告里实际 0.5，未显式记录。

## 根因
评估脚本多个 IoU/conf 参数含义未分离、未落盘；汇报口径不统一。

## 证据
- IoU 笔误事件（`min(by2,by2)` 导致 FN/FP 高估 2.6x/1.5x）；
- NMS=0.45 复评：所有模型 mAP50-95 下滑（balanced q2000 −0.034），固定 conf 下 F1 升但 FN 增；
- 线上最优工作点实测 conf≈0.45~0.50，NMS 保持 0.7。

## 处置
- 脚本显式分离 `--conf / --nms-iou / --match-iou` 并写入 run_config；
- mAP 与固定阈值 F1 分开汇报；
- badcase 归因固定 conf=0.25（放大镜），汇报主表 conf=0.45。

## 预防
- 对数字先报口径（conf/NMS/match/测试集）；
- 评估输出目录记录完整协议。
