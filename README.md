# Personal Wiki

一个以 Markdown 为主、Jupyter Notebook 为辅的个人知识库，面向开发、科研和持续学习。仓库保留论文、教材与课程笔记的完整上下文，同时通过概念页、知识地图、稳定章节锚点和相对链接形成可搜索、可跳转的知识网络。

## 核心模型

本项目不假设“一个 Markdown 文件就是一个原子词条”。这里区分三类知识对象：

| 类型 | 目录 | 组织依据 | 主要职责 |
| --- | --- | --- | --- |
| 来源笔记 | `docs/notes/` | 论文、教材、课程 | 保留来源的论证顺序、推导和完整上下文 |
| 概念页 | `docs/concepts/` | 概念、定理、方法 | 综合多个来源，提供稳定的跨来源入口 |
| 知识地图 | `docs/maps/` | 领域或学习路径 | 表达领域边界、先修关系和推荐阅读顺序 |

文件负责保存上下文，标题锚点提供细粒度跳转，概念页负责跨来源综合。目录只表达内容类型和粗粒度归属，正文链接才表达真正的知识关系。

## 设计原则

- **对象独立**：每个来源笔记、概念页或知识地图都是一个独立文件夹，入口固定为 `index.md`。
- **来源完整**：不为了追求短词条而机械拆分论文、教材和课程笔记。
- **节点可寻址**：长笔记中重要章节使用稳定锚点，可以被其他内容精确引用。
- **按需综合**：一个概念被多个来源引用或需要长期维护时，才提升为独立概念页。
- **资料共置**：对象专用的图片、Notebook 和补充材料与其 `index.md` 放在同一文件夹中。
- **通用链接**：使用标准相对 Markdown 链接，兼容编辑器、Git 托管平台和构建后的站点。
- **可持续维护**：本地检查发现错误目录、对象类型、缺失元数据和断开的本地链接。

## 仓库结构

```text
Personal-Wiki/
├── AGENTS.md
├── README.md
├── mkdocs.yml
├── requirements.txt
├── Makefile
├── docs/
│   ├── index.md                              # 站点门户
│   ├── tags.md                               # 标签索引
│   ├── assets/                               # 多对象共享资源
│   ├── notes/
│   │   ├── papers/<paper-slug>/
│   │   │   ├── index.md                      # 论文长笔记
│   │   │   ├── assets/
│   │   │   ├── notebooks/
│   │   │   └── sources/
│   │   ├── books/<book-slug>/
│   │   │   └── index.md                      # 教材或专著长笔记
│   │   └── courses/<course-slug>/
│   │       └── index.md                      # 课程长笔记
│   ├── concepts/<domain>/<concept-slug>/
│   │   └── index.md                          # 跨来源概念页
│   └── maps/<domain>/
│       └── index.md                          # 领域知识地图
├── templates/
│   ├── notes/
│   │   ├── paper/index.md
│   │   ├── book/index.md
│   │   └── course/index.md
│   ├── concept/index.md
│   └── map/index.md
└── scripts/
    └── check_wiki.py
```

`docs/index.md`、`docs/tags.md` 和 `docs/assets/` 是站点基础设施，不属于知识对象。每个实际内容对象都必须位于自己的文件夹中。

目录名使用小写 ASCII 字母、数字和连字符，例如：

```text
docs/notes/papers/einstein-podolsky-rosen/
docs/notes/books/quantum-optics-introduction/
docs/concepts/quantum-optics/wigner-function/
docs/maps/continuous-variable-quantum-information/
```

## 快速开始

仓库使用 Python 虚拟环境和 MkDocs Material：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
make serve
```

常用命令：

```bash
make check   # 检查对象结构、元数据和本地链接
make build   # 严格模式构建静态站点到 site/
make serve   # 启动带自动刷新的本地预览
```

## 编写来源笔记

根据来源类型复制模板：

```bash
cp -r templates/notes/paper docs/notes/papers/paper-slug
cp -r templates/notes/book docs/notes/books/book-slug
cp -r templates/notes/course docs/notes/courses/course-slug
```

来源笔记可以很长，应优先保留材料原有的论证、推导和课程结构。核心结论仍需在 Markdown 中说明，Notebook 用于复现、计算或实验，不代替可搜索的文字总结。

论文、教材和课程分别使用 `paper-note`、`book-note` 和 `course-note` 作为 `kind`。模板还提供作者、年份、DOI、ISBN、机构、教师等来源元数据占位符。

## 在长笔记中创建稳定节点

普通标题已经可以产生网页锚点，但标题文字改变时链接也可能失效。对于会被其他页面频繁引用的章节，在标题前添加稳定的英文 ID：

```html
<a id="wigner-function"></a>

## Wigner 函数
```

其他对象可以精确链接到这一节：

```markdown
[教材中的 Wigner 函数推导](../../../notes/books/book-slug/index.md#wigner-function)
```

因此，知识网络中的节点既可以是完整对象，也可以是“对象路径 + 章节锚点”。不要仅为了获得跳转能力把连贯笔记拆成许多短文件。

## 创建概念页

当一个概念满足以下任一条件时，可以从 `templates/concept/` 创建概念页：

- 被多个论文、课程或教材引用；
- 不同来源的定义、符号或适用条件需要比较；
- 需要一个不依赖单一来源的稳定入口；
- 需要持续整理其前置概念、应用或常见误区。

```bash
cp -r templates/concept docs/concepts/domain/concept-slug
```

概念页应综合而不是复制来源笔记。它需要链接到支撑结论的具体笔记章节，并说明不同来源各自承担的作用。

## 创建知识地图

知识地图用于表达领域结构和推荐阅读路径：

```bash
cp -r templates/map docs/maps/domain
```

一张地图通常列出先修知识、核心概念、来源材料、建议顺序和开放问题。它不是内容目录的重复，而是带有关系说明的学习导航。

当前架构示例见 [Personal Wiki 架构地图](docs/maps/meta/index.md)。

## 元数据契约

所有知识对象至少包含：

```yaml
---
title: 人类可读标题
kind: concept
tags:
  - 标签
status: seed
updated: 2026-08-08
---
```

当前允许的 `kind` 与目录对应关系：

| 路径 | `kind` |
| --- | --- |
| `docs/notes/papers/<slug>/index.md` | `paper-note` |
| `docs/notes/books/<slug>/index.md` | `book-note` |
| `docs/notes/courses/<slug>/index.md` | `course-note` |
| `docs/concepts/<domain>/<slug>/index.md` | `concept` |
| `docs/maps/<domain>/index.md` | `map` |

建议的成熟度状态：

- `seed`：已有轮廓，仍待扩充；
- `growing`：主要内容已形成，仍在迭代；
- `evergreen`：结构稳定并经过复核，但仍可继续更新。

标签用于横向发现，目录用于内容分类，链接用于语义关系，三者不相互替代。

## 链接和资源约定

- 对象链接显式指向 `index.md`，例如 `[交叉链接](../cross-link/index.md)`；MkDocs 会将它转换为目录 URL。
- 章节链接追加稳定锚点，例如 `index.md#wigner-function`。
- 链接应附带关系说明，避免无语义的链接堆积。
- 对象专用资源放入该对象的 `assets/`、`notebooks/` 或 `sources/`。
- 只有被多个对象共同使用的资源才放在 `docs/assets/`。
- Notebook 提交前应清理无价值的大型输出和敏感数据。

更具体的 Markdown、Notebook、公式、引用和写作规范后续维护在 [AGENTS.md](AGENTS.md) 中。
