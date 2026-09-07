---
tags: [train, pretrained, grid]
status: 已处置（2026-09，记录用）
---

# 预训练权重损坏导致启动崩溃（E9）

## 现象
E9（grid6490 从 COCO 预训练重训）尝试启动即失败：`PytorchStreamReader failed reading
zip archive: failed finding central directory`，从未进入训练。

## 根因
当时 `yolov8m.pt` 未下载完整/损坏（08:56 才补齐，启动发生在 08:39）。

## 证据
- `/ya/Code/ljh/yolo_grid/results/exp0828/e9/e9_retrain_coco_train.log`。

## 处置
- 修复/重下权重后再跑（本项目后续未重跑 E9，COCO 方向由对方 09-01 实验覆盖）。

## 预防
- 训练启动前校验权重文件大小/可加载（torch.load + 字节数）；
- 下载过程用 sha256 校验（对方 coco 实验目录留有 `yolov8m.pt.sha256`）。
