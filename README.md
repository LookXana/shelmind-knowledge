# shelfmind-knowledge

个人/团队可迁移的 AI 协作知识仓：把跨任务经验、各业务的路由与坑点放在一个独立 git 仓，
业务项目只放指向本仓的薄指针（AGENTS.md）。

## 结构

```text
shelfmind-knowledge/
├── AGENTS.md              知识仓工作契约
├── config.yaml            模块清单 + 本机路径映射
├── developers.yaml        成员与模块负责人
├── global/                跨任务规范与经验
├── spec/
│   ├── grid/             棚格检测（路由 + bugs）
│   └── esl-ocr/          电子价签 OCR（路由 + bugs，内容待蒸馏）
├── workflows/             超参/流程白名单（供校验拦截）
├── scripts/validate.py    结构校验
├── runtime/               （本机，gitignore）会话/任务台账
└── tasks/                 （本机，gitignore）长任务卡
```

## 用法

1. 新开任意业务项目：在项目根放 `AGENTS.md` 薄指针，指向本仓 `spec/<业务>/index.md`；
2. AI 助手/同事按 index 路由去读业务文档与 bugs；
3. 踩坑后按 bug 模板 append 进本仓，业务项目不复制；
4. 提交前跑 `python scripts/validate.py`。

## 迁移状态

- [x] 知识仓骨架与契约
- [x] `spec/grid/` 首批坑点蒸馏（2026-09-07）
- [x] `D:\yolo_pengge\AGENTS.md` 薄指针
- [ ] `spec/esl-ocr/` 内容蒸馏（原料已定位）
- [ ] Qoder 原生 knowledges 同步策略验证
- [ ] 远程私有仓（待定，不影响本地使用）
