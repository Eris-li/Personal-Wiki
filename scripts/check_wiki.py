#!/usr/bin/env python3
"""Validate Personal Wiki object layouts, metadata, and local links."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTES = DOCS / "notes"
CONCEPTS = DOCS / "concepts"
MAPS = DOCS / "maps"

NOTE_KINDS = {
    "papers": "paper-note",
    "books": "book-note",
    "courses": "course-note",
}
COMMON_REQUIRED_FIELDS = {"title", "kind", "tags", "status", "updated"}
ALLOWED_STATUS = {"seed", "growing", "evergreen"}
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def display(path: Path) -> str:
    """Return a repository-relative path for readable diagnostics."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_slug(path: Path, label: str) -> list[str]:
    if SLUG_RE.fullmatch(path.name):
        return []
    return [f"{display(path)}: {label}必须使用小写英文数字和单个连字符"]


def validate_notes() -> tuple[dict[Path, str], list[str]]:
    objects: dict[Path, str] = {}
    errors: list[str] = []
    if not NOTES.is_dir():
        return objects, [f"{display(NOTES)}: 来源笔记根目录不存在"]

    actual_types = {path.name for path in NOTES.iterdir() if path.is_dir()}
    unknown_types = actual_types - NOTE_KINDS.keys()
    for name in sorted(unknown_types):
        errors.append(
            f"{display(NOTES / name)}: 未知来源类型；新增类型时需同步模板和检查规则"
        )

    for source_type, expected_kind in NOTE_KINDS.items():
        category = NOTES / source_type
        if not category.is_dir():
            errors.append(f"{display(category)}: 缺少来源分类目录")
            continue
        for note in sorted(path for path in category.iterdir() if path.is_dir()):
            errors.extend(validate_slug(note, "来源笔记目录名"))
            index = note / "index.md"
            if not index.is_file():
                errors.append(f"{display(note)}: 缺少来源笔记入口 index.md")
            else:
                objects[index] = expected_kind

    expected_markdown = set(objects)
    for markdown in sorted(NOTES.rglob("*.md")):
        if markdown not in expected_markdown:
            errors.append(
                f"{display(markdown)}: 来源笔记 Markdown 必须位于 "
                "notes/<papers|books|courses>/<note>/index.md"
            )
    return objects, errors


def validate_concepts() -> tuple[dict[Path, str], list[str]]:
    objects: dict[Path, str] = {}
    errors: list[str] = []
    if not CONCEPTS.is_dir():
        return objects, [f"{display(CONCEPTS)}: 概念页根目录不存在"]

    for domain in sorted(path for path in CONCEPTS.iterdir() if path.is_dir()):
        errors.extend(validate_slug(domain, "概念领域目录名"))
        for concept in sorted(path for path in domain.iterdir() if path.is_dir()):
            errors.extend(validate_slug(concept, "概念目录名"))
            index = concept / "index.md"
            if not index.is_file():
                errors.append(f"{display(concept)}: 缺少概念页入口 index.md")
            else:
                objects[index] = "concept"

    expected_markdown = set(objects)
    for markdown in sorted(CONCEPTS.rglob("*.md")):
        if markdown not in expected_markdown:
            errors.append(
                f"{display(markdown)}: 概念页 Markdown 必须位于 "
                "concepts/<domain>/<concept>/index.md"
            )
    return objects, errors


def validate_maps() -> tuple[dict[Path, str], list[str]]:
    objects: dict[Path, str] = {}
    errors: list[str] = []
    if not MAPS.is_dir():
        return objects, [f"{display(MAPS)}: 知识地图根目录不存在"]

    for domain in sorted(path for path in MAPS.iterdir() if path.is_dir()):
        errors.extend(validate_slug(domain, "知识地图领域目录名"))
        index = domain / "index.md"
        if not index.is_file():
            errors.append(f"{display(domain)}: 缺少知识地图入口 index.md")
        else:
            objects[index] = "map"

    expected_markdown = set(objects)
    for markdown in sorted(MAPS.rglob("*.md")):
        if markdown not in expected_markdown:
            errors.append(
                f"{display(markdown)}: 知识地图 Markdown 必须位于 maps/<domain>/index.md"
            )
    return objects, errors


def validate_layout() -> tuple[dict[Path, str], list[str]]:
    objects: dict[Path, str] = {}
    errors: list[str] = []
    for validator in (validate_notes, validate_concepts, validate_maps):
        found, found_errors = validator()
        objects.update(found)
        errors.extend(found_errors)
    if not objects:
        errors.append("docs: 至少需要一个知识对象")
    return objects, errors


def parse_front_matter(path: Path, text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [f"{display(path)}: 缺少 YAML front matter"]

    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}, [f"{display(path)}: YAML front matter 未闭合"]

    front_lines = lines[1:end]
    fields: dict[str, str] = {}
    for line in front_lines:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if match:
            fields[match.group(1)] = (match.group(2) or "").strip().strip("'\"")

    missing = COMMON_REQUIRED_FIELDS - fields.keys()
    if missing:
        errors.append(
            f"{display(path)}: 缺少元数据字段 {', '.join(sorted(missing))}"
        )

    if fields.get("status") and fields["status"] not in ALLOWED_STATUS:
        errors.append(
            f"{display(path)}: status 必须是 {', '.join(sorted(ALLOWED_STATUS))} 之一"
        )

    updated = fields.get("updated", "")
    if updated:
        if not DATE_RE.fullmatch(updated):
            errors.append(f"{display(path)}: updated 必须使用 YYYY-MM-DD")
        else:
            try:
                date.fromisoformat(updated)
            except ValueError:
                errors.append(f"{display(path)}: updated 不是有效日期")

    tags_line = next(
        (i for i, line in enumerate(front_lines) if re.match(r"^tags:", line)), None
    )
    if tags_line is not None:
        inline_tags = front_lines[tags_line].split(":", 1)[1].strip()
        if inline_tags in {"[]", "null", "~"}:
            errors.append(f"{display(path)}: tags 必须包含至少一个标签")
        elif not inline_tags:
            tag_items = []
            for line in front_lines[tags_line + 1 :]:
                if line and not line[0].isspace():
                    break
                if re.match(r"^\s+-\s+\S", line):
                    tag_items.append(line)
            if not tag_items:
                errors.append(f"{display(path)}: tags 必须包含至少一个标签")

    return fields, errors


def local_link_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target or target.startswith(
        ("http://", "https://", "mailto:", "tel:", "/")
    ):
        return None
    resolved = (source.parent / target).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return Path("/__outside_repository__")
    return resolved


def without_fenced_code(text: str) -> str:
    """Remove fenced code blocks so examples are not treated as real links."""
    visible_lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            visible_lines.append("")
        elif fence is None:
            visible_lines.append(line)
        else:
            visible_lines.append("")
    return "\n".join(visible_lines)


def validate_links(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for raw_target in LINK_RE.findall(without_fenced_code(text)):
        target = local_link_target(path, raw_target)
        if target is None:
            continue
        if target.name == "__outside_repository__":
            errors.append(f"{display(path)}: 本地链接越出仓库范围: {raw_target}")
        elif target.is_dir() and not (target / "index.md").is_file():
            errors.append(f"{display(path)}: 目录链接缺少 index.md: {raw_target}")
        elif not target.exists():
            errors.append(f"{display(path)}: 本地链接目标不存在: {raw_target}")
    return errors


def main() -> int:
    objects, errors = validate_layout()
    markdown_files = sorted(DOCS.rglob("*.md"))
    counts = {"note": 0, "concept": 0, "map": 0}

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        errors.extend(validate_links(path, text))
        if path in objects:
            fields, metadata_errors = parse_front_matter(path, text)
            errors.extend(metadata_errors)
            expected_kind = objects[path]
            actual_kind = fields.get("kind")
            if actual_kind and actual_kind != expected_kind:
                errors.append(
                    f"{display(path)}: 路径要求 kind: {expected_kind}，"
                    f"当前为 {actual_kind}"
                )
            if expected_kind.endswith("-note"):
                counts["note"] += 1
            else:
                counts[expected_kind] += 1

    if errors:
        print(f"Wiki 检查失败（{len(errors)} 个问题）：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Wiki 检查通过："
        f"{counts['note']} 篇来源笔记，"
        f"{counts['concept']} 个概念页，"
        f"{counts['map']} 张知识地图，"
        f"{len(markdown_files)} 个站点页面。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
