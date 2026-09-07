# shelfmind-knowledge 工作契约

本仓是团队知识的**唯一真源**；各业务项目只放薄指针，不复制知识。

## 规则

1. **分层写入**：跨任务知识进 `global/`；业务知识进 `spec/<业务>/index.md`；
   具体坑点进 `spec/<业务>/bugs/`（一个坑一个文件，用统一模板）。
2. **append-only**：新结论=新增文件或追加小节；旧结论修正时标记 `deprecated` 并链接新条目，
   不重写历史，方便同事追溯。
3. **路径不写死**：文档内一律用占位符（`<GRID_ROOT>`、`<ESL_OCR_ROOT>`）；
   实际映射写在 `config.yaml`（本机覆盖放 `path_maps.local.yaml`，gitignore）。
4. **禁止入仓**：密码/密钥/令牌、内网敏感地址、个人隐私；服务器操作默认只读。
5. **bug 模板字段**：现象 / 根因 / 证据 / 处置 / 预防 / 状态（与业务侧 bug_ledger 一致）。
6. **改动校验**：提交前运行 `python scripts/validate.py`，PASS 才能提交。
7. **协作纪律**：小步提交；不 force push 共享分支；多人合入用 PR/review 语义。
8. **AI 助手使用时**：先读 `spec/<业务>/index.md` 再决定要不要展开 bugs/；业务代码不碰，
   沉淀知识一律走本仓（append）。

## 常用命令（MVP 阶段）

```text
python scripts/validate.py          # 结构/模板校验
git add -A && git commit            # 本地版本管理
```

（`shelf` CLI 的 task/ledger/recover 等子命令等有真实需求再补。）
