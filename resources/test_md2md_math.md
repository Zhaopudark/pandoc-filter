# 数学公式的基本概念

- 需要在pandoc生成命令中，添加 --mathjax 才能启用公式
- 公式中 \label 和\tag区别
  - `\label` 用于打上内部标签，配合引用`\ref{标签}`
  - `\tag` 用于显式地对公式编号。是一种外部展示。文本课件公式的编号，和引用时对公式的指代。
  - 若`\ref{标签}`引用的公式最终没有tag，一般会出现???的显示

## 行内公式

需要严格按照`$xxxx$`的形式，`$`符号的的最近邻不能有空格，否则会存在部分或全部元素丢失。

- 正常情况：

  - `$e=mc^2 \rightarrow$`: $e=mc^2 \rightarrow$

- `$`符号的的最近邻有空格：

  - `$ \rightarrow$`: $ \rightarrow$

  - `$\inf $`: $\inf $

## 公式块（行间公式）和自动编号

NOTICE: 统一采用 AMS规则

$$
\begin{equation}\tag{abcd}\label{lalla}
e=mc^2
\end{equation}
$$

`Use AMS Numbering Rule (where only certain environments produce numbered equations, as they would be in LaTeX).`

即只对：`equation`框定的模块且标注的公式自动编号

```latex
\begin{equation}
e=mc^2
\end{equation}
```



$$
\begin{equation}
e=mc^2
\end{equation}
$$

## 公式块（行间公式）标注和引用

$$
\begin{equation}\label{eq1}
e=mc^2
\end{equation}
$$

对公式2的定义语法为：

```latex
\begin{equation}\label{eq1}
e=mc^2
\end{equation}
```

此处使用语法`$公式\label{eq1}$`进行引用，效果为：引用 $公式\ref{eq1}$
此处使用语法`$公式\label{eq1}$`进行引用，效果为：引用 $公式\ref{lalla}$

## 公式块（行间公式）换行

使用`\displaylines{x+y\\y+z}`语法换行

$$
\displaylines{x+y\\y+z}
$$


使用`\\`换行

$$
x+y\\y+z
$$

使用`\\\\`换行

$$
x+y\\\\y+z
$$

使用`\newline`换行

$$
x+y\newline y+z
$$

使用`aligned` 块换行

$$
\begin{aligned}
&x+y \\
&y+z
\end{aligned}
$$

## 公式块（行间公式）中遇到中文

$$
x+y\\y+z
\\
这是中文\\
$$
