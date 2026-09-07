# esl-ocr（电子价签 OCR / VLM）路由

## 状态

- 内容**待蒸馏**：本页只做路由，业务细节以业务仓为准；
- bugs/ 目前为空，条目从原料文档提炼后再落盘。

## 项目位置（只读指针）

- 业务仓（git）：`<ESL_OCR_ROOT>`；
- 已有复盘/技术文档（勿复制进知识仓，蒸馏时引用）：
  - `GRPO复盘笔记.md`
  - `GKD蒸馏实验复盘.md`
  - `后训练与LoRA入门.md`
  - `电子价签OCR_VLM训练蒸馏与端侧部署_技术报告.docx`
  - `HunyuanOCR_Agentic_Data_Flow_详解与ESL-OCR迁移.docx`

## 待蒸馏主题（逐条核对后转 bugs/，当前不是结论）

- reward 退化 / 多奖励尺度失衡（GRPO）；
- 小图下采样导致的识别损失；
- 蒸馏失配（GKD/teacher-student）；
- LoRA 超参与层选择；
- 端侧部署量化（FP16/INT8）误差。

## 关联知识

- 跨任务训练/评测纪律见 `global/训练评测规范.md`；
- GRPO/蒸馏候选坑点见 `global/GRPO与多奖励坑点.md`、`global/蒸馏与LoRA坑点.md`（同为待蒸馏）。

## 迁移计划

- [ ] 通读 4 份原料文档，按 bug 模板提炼 3~5 条首批坑点；
- [ ] 为 GRPO 实验补 workflows 白名单（reward 组合/采样参数）；
- [ ] 验证：跑一条"GRPO 复现任务卡 + 崩溃恢复"。
