---
title: 交叉链接
aliases:
  - 内部链接
kind: concept
tags:
  - knowledge-management
  - navigation
status: growing
updated: 2026-08-08
---

# 交叉链接

交叉链接是在[知识对象](../knowledge-object/index.md)或其内部章节之间建立的显式连接。目录只表达一种归属关系，链接则能连接分布在论文、课程、教材和概念综合页中的相关知识。

## 两种链接粒度

链接整个对象时，显式指向它的入口文件：

```markdown
[知识对象](../knowledge-object/index.md)
```

链接长笔记中的具体知识时，指向稳定章节锚点：

```markdown
[Wigner 函数的推导](../../../notes/books/example-book/index.md#wigner-function)
```

对会被外部笔记频繁引用的章节，建议在标题前定义稳定的英文锚点：

```html
<a id="wigner-function"></a>

## Wigner 函数
```

这样标题措辞可以调整，而已有链接不必随之改变。

## 链接原则

链接应出现在关系最容易理解的上下文中，并说明目标内容为何相关。长笔记可以在章节末列出相关概念和其他来源；概念页则应链接到支撑其结论的具体笔记章节。不要为了链接数量机械堆积无关关系。

## 关联概念

- [知识对象](../knowledge-object/index.md)：交叉链接所连接的内容单元。
