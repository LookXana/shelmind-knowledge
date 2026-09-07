"""shelfmind-knowledge 结构校验（MVP，纯 stdlib）。

用法: python scripts/validate.py [repo_root]
检查: 顶层必需文件、spec/<模块>/index.md、bugs 模板字段、workflows 文件存在。
"""
import sys
from pathlib import Path

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent

TOP_REQUIRED = ["AGENTS.md", "README.md", "config.yaml", "developers.yaml", ".gitignore"]
GLOBAL_REQUIRED = ["训练评测规范.md"]
BUG_FIELDS = ["## 现象", "## 根因", "## 证据", "## 处置", "## 预防"]


def yaml_lines(path: Path) -> bool:
    return path.exists() and path.suffix.lower() in (".yaml", ".yml")


def main() -> int:
    errors: list[str] = []
    for name in TOP_REQUIRED:
        if not (REPO / name).exists():
            errors.append(f"缺少顶层文件: {name}")
    for name in GLOBAL_REQUIRED:
        if not (REPO / "global" / name).exists():
            errors.append(f"缺少 global 文件: {name}")

    # 模块与 index
    cfg = (REPO / "config.yaml").read_text(encoding="utf-8", errors="ignore")
    for line in cfg.splitlines():
        line = line.strip()
        if line.startswith("index: spec/"):
            idx = REPO / line.split("index: ", 1)[1]
            if not idx.exists():
                errors.append(f"config 指向的 index 不存在: {idx}")

    # bugs 模板
    for bug in sorted((REPO / "spec").glob("*/bugs/*.md")):
        text = bug.read_text(encoding="utf-8", errors="ignore")
        for field in BUG_FIELDS:
            if field not in text:
                errors.append(f"{bug.relative_to(REPO)} 缺少字段: {field}")
        if not text.lstrip().startswith("---"):
            errors.append(f"{bug.relative_to(REPO)} 缺少 front-matter")

    # workflows
    wf_dir = REPO / "workflows"
    if wf_dir.exists():
        wf = list(wf_dir.glob("*.yaml"))
        if not wf:
            errors.append("workflows/ 为空")
        for p in wf:
            if ":" not in p.read_text(encoding="utf-8", errors="ignore"):
                errors.append(f"{p.name} 不是有效 YAML（缺冒号）")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print(f"PASS ({REPO})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
