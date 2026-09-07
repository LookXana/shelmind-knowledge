---
tags: [infra, concurrency, ultralytics]
status: 已处置（2026-08/09）
---

# Ultralytics .cache 并发竞争

## 现象
共享数据集上并行启动多个训练/评估：不同 manifest 的哈希不同，进程互相删除
`labels/train.cache` 等文件，触发 FileNotFoundError（failed_cache_race_* 目录为现场）。

## 根因
Ultralytics 即使 cache=False 也会在共享 labels 目录写/删 cache；无锁并发扫描冲突。

## 证据
- `failed_cache_race_20260903_0914`、`grid_260330_cache_race_20260903_094359` 等失败现场目录；
- 报告 §6.2 无效启动记录（并发下载/扫描类问题多次出现）。

## 处置
- 标签变更后先删旧 .cache；
- 首组任务先单独完成数据扫描进入训练后，再启动第二组；
- 分来源评估用 `--eval-lock` 串行。

## 预防
- 共享数据只读；缓存预热与评估锁写进启动脚本；
- 失败目录保留，便于按现场排查。
