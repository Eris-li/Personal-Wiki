# AGENTS.md

本文件定义整个仓库的架构约束和自动化协作方式。若更深层目录以后出现自己的 `AGENTS.md`，其规则只在对应子树内补充或覆盖本文件。

## 项目定位

这是一个面向开发与科研背景知识的 Personal Wiki。Markdown 是长期可读的主要载体，Jupyter Notebook 是推导、实验和演示的辅助材料。知识通常来自论文、教材和课程，因此必须保留来源上下文，同时通过概念综合、知识地图和细粒度链接建立知识网络。

## 内容模型

仓库包含三类知识对象：

- `docs/notes/`：按论文、教材或课程组织的长篇来源笔记；
- `docs/concepts/`：综合多个来源的概念、定理或方法页面；
- `docs/maps/`：表达领域边界、先修关系和推荐阅读路径的知识地图。

文件不是知识网络中唯一的节点。长篇笔记中带稳定锚点的章节也是可链接节点。不要为了模拟原子词条而破坏论文、教材或课程笔记的连贯结构。

## 架构约束

- Wiki 源文件位于 `docs/`，构建产物 `site/` 不提交。
- `docs/index.md` 是站点门户，`docs/tags.md` 是标签索引；两者都不是知识对象。
- 每个知识对象独占一个文件夹，入口必须命名为 `index.md`。
- 来源笔记路径为：
  - `docs/notes/papers/<note-slug>/index.md`，`kind: paper-note`；
  - `docs/notes/books/<note-slug>/index.md`，`kind: book-note`；
  - `docs/notes/courses/<note-slug>/index.md`，`kind: course-note`。
- 概念页路径为 `docs/concepts/<domain>/<concept-slug>/index.md`，并使用 `kind: concept`。
- 知识地图路径为 `docs/maps/<domain>/index.md`，并使用 `kind: map`。
- `<domain>` 和各种 `<slug>` 使用小写 ASCII 字母、数字及单个连字符；不要使用空格、下划线或中文目录名。显示名称写入 front matter 的 `title`。
- 不要在上述内容根目录、分类目录或对象资源子目录中放置散落的 Markdown 页面。需要成为独立页面的内容必须拥有自己的对象文件夹。
- 对象专用图片、Notebook 和资料分别优先放在该对象的 `assets/`、`notebooks/`、`sources/` 中；只有多对象共享资源才放 `docs/assets/`。

## 链接约束

- 使用标准相对 Markdown 链接，不要引入只受特定编辑器支持的 `[[WikiLink]]` 语法。
- 链接完整对象时显式指向其入口，例如 `[交叉链接](../cross-link/index.md)`。MkDocs 构建时会转换为目录 URL。
- 链接长笔记的具体知识时使用 `index.md#stable-anchor`。
- 会被其他对象频繁引用的章节应在标题前添加稳定、语义化的英文锚点：

  ```html
  <a id="wigner-function"></a>

  ## Wigner 函数
  ```

- 链接附近应说明前置、来源、对比、应用或延伸关系，避免只有链接列表而没有语义。
- 移动对象、重命名目录或调整稳定锚点前，必须用 `rg` 搜索所有入链并同步更新。

## 内容边界

- 来源笔记负责忠实记录和理解一份论文、教材或课程，允许较长，不要求适配概念页模板。
- 概念页负责跨来源综合。不要把某一份来源笔记全文复制到概念页；应链接到支撑结论的具体章节。
- 只有当概念被多个来源引用、需要比较定义或值得长期维护时，才新建独立概念页。
- 知识地图负责关系和阅读路径，不应退化为自动目录或无说明的链接集合。
- 核心结论、假设和解释必须写在 Markdown 中。Notebook 是复现或扩展材料，不能成为唯一说明。

## 修改流程

1. 修改前阅读根目录 `README.md`，确认对象类型、来源和相邻内容。
2. 新对象使用对应模板：
   - `templates/notes/paper/index.md`；
   - `templates/notes/book/index.md`；
   - `templates/notes/course/index.md`；
   - `templates/concept/index.md`；
   - `templates/map/index.md`。
3. 填写必需元数据并删除模板占位符；来源笔记还应填写可获得的出处信息。
4. 内容变更应补充有意义的上下文链接，但不要为了链接数量制造无关关系。
5. 不改写与任务无关的用户笔记，不清除 Notebook 输出，除非任务明确要求。
6. 完成后运行：

   ```bash
   python scripts/check_wiki.py
   mkdocs build --strict
   ```

7. 若仅修改仓库说明或非站点文件，至少运行 `python scripts/check_wiki.py`。

## 当前元数据契约

所有知识对象的 `index.md` 必须包含 YAML front matter，并至少提供：

- `title`：人类可读标题；
- `kind`：与所在目录匹配的对象类型；
- `tags`：包含至少一个标签的 YAML 列表；
- `status`：使用 `seed`、`growing` 或 `evergreen`；
- `updated`：最后一次实质更新日期，格式为 `YYYY-MM-DD`。

正文应只有一个一级标题，且建议与 `title` 一致。论文、教材和课程的出处字段目前由模板引导，但尚未作为统一的机械检查规则。

## 自动检查边界

`scripts/check_wiki.py` 检查可机械判定的规则：对象目录、入口文件、路径与 `kind` 的对应关系、必需元数据、状态、日期和本地 Markdown 链接。它不替代事实核查、公式验证、锚点语义稳定性、引用质量或写作审阅。

## 后续笔记规范（预留）

后续可在此处增加 Markdown、Notebook、数学公式、代码示例、参考文献、图片版权、命名和语言风格规范。新增规范时应说明适用对象，并同步更新对应模板和自动检查；不要让文档规则与工具行为相互矛盾。
