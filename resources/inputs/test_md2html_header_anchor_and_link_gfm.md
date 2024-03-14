---
title: test_md2html_anchor_and_link_gfm
---
# 引用链接

## 超链接

语法：`[Link Text](link-address)`

效果：[Links - Typora Support
(typoraio.cn)](https://support.typoraio.cn/Links/)

## 参考链接

语法：

``` markdown
[Link Text][Ref2] 

[Ref2]: https://support.typoraio.cn/Links/  "typora links"
```

效果（自动转为普通超链接）：

[Link Text](https://support.typoraio.cn/Links/ "typora links")

## 自动链接和网址

语法：`<http://typora.io>`

效果：<http://typora.io>

语法：`This is a link: http://typora.io`

效果：This is a link: http://typora.io

## 本地资源链接

语法：参考[Links - Typora Support
(typoraio.cn)](https://support.typoraio.cn/Links/#link-to-local-files)

- 不确保非站内资源可行。

- 不应该支持非站内资源，但是难以排除这些目的之外的资源。

``` markdown
[404_page](../404.html)
[this_page](../posts/d36d5fbd.html)
```

[404_page](../404.html)

[this_page](../posts/d36d5fbd.html)

## 页内链接(链接到headings锚点和raw-HTML锚点)

- 当headings中含有大小写时，允许链接不区分大小写

  #### A.1

  ## Second_level

  [跳转到Second_level,#Second_level](#Second_level)

  [跳转到Second_level,#second_level](#second_level)

  ## ErJi目lu

  [跳转到ErJi目lu,#ErJi目lu](#ErJi目lu)

  [跳转到ErJi目lu,#erji目lu](#erji目lu)

  [\#a.1](#a.1)

- raw-HTML锚点与raw-HTML跳转

  ``` html
  <a id="anchor1"></a> Anchor

  <a href="#anchor1">Link to Anchor</a>
  ```

  定义raw-HTML锚点<a id="anchor1">anchor1</a>

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  <a href="#anchor1">raw-HTML跳转到 anchor1</a>

- 带有特殊字符时，简化并改变了一般的Markdown渲染html的规则

  - 不遵从Typora的[internal-links](https://support.typoraio.cn/Links/#internal-links)语法
  - 直接将原内容复制到`[]()`的`()`内即可
  - 推荐使用上述方式，也只保证上述方式是可行的
  - 其余方式可能会出现意外结果

  ## 带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试 空格

  ### aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz \[xx\] (yy)

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  - 使用markdown语法的链接到headings锚点
    - [带空格 和`特殊字符` \[链接\](http://typora.io)
      用于%%%%￥￥￥￥跳转测试
      空格](#带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试 空格)
    - [aAa-b cC `Dd`, a#%&\[xxx\](yyy) Zzz \[xx\]
      (yy)](#aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz \[xx\] (yy))
  - 使用raw-HTML链接到headings锚点
    - <a href="#带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试 空格">带空格
      和`特殊字符`…</a>
    - <a href="#aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz \[xx\] (yy)">aAa-b…</a>

- 链接允许多重#号

  # 一级目录

  ## 二级目录

  ### 三级目录

  #### 四级目录

  ##### 五级目录

  ###### 六级目录

  [跳转到一级目录,且是单个#号,#一级目录](#一级目录)

  [跳转到一级目录但是2个#号,##一级目录](#一级目录)

  [跳转到二级目录但是单个#号,#二级目录](#二级目录)

  [跳转到二级目录但是2个#号,##二级目录](#二级目录)

  [跳转到三级目录但是单个#号,#三级目录](#三级目录)

  [跳转到三级目录但是3个#号,###三级目录](#三级目录)

  [跳转到四级目录但是单个#号,#四级目录](#四级目录)

  [跳转到四级目录但是4个#号,####四级目录](#四级目录)

  [跳转到五级目录但是单个#号,#五级目录](#五级目录)

  [跳转到五级目录但是5个#号,#####五级目录](#五级目录)

  [跳转到六级目录但是单个#号,#六级目录](#六级目录)

  [跳转到六级目录但是6个#号,######六级目录](#六级目录)

  <a href="#六级目录">raw-HTML跳转到六级目录但是6个#号</a>

- 锚点自动追加`-x`,
  `x`为数字以区分。从`-1`开始，重复时数字+1。链接可能带有`-x`结尾，当存在与链接内容(包括`-x`)完全一致的锚点时，跳转到该锚点，不存在这样的锚点时，跳转到与链接剔除`-x`后的内容完全一致的第`x`个锚点。即：

  - 优先全文匹配
  - 其次按序号匹配
  - 需要确保上述匹配过程，至少有一个锚点是存在的。若这样的锚点不存在，渲染器手动抛出异常提醒。

  ## hello

  二级目录 hello

  # hello

  一级目录 hello

  # hello-2

  一级目录 hello

  ### hello

  三级目录 hello

  ##### hello

  五级目录 hello

  ### hello

  三级目录 hello

  <a id="hello">hello</a>

  自定义锚点 hello

  [跳转到第1次出现的二级目录hello,#hello](#hello)

  [跳转到第1次出现的二级目录hello,#hello-0](#hello-0)

  [跳转到第1次出现的一级目录hello,#hello-1](#hello-1)

  [跳转到一级目录hello-2,#hello-2](#hello-2)

  [跳转到第3次出现的三级目录hello,#hello-3](#hello-3)

  [跳转到第4次出现的五级目录hello,#hello-4](#hello-4)

  [跳转到第5次出现的三级目录hello,#hello-5](#hello-5)

  [跳转到第6次出现的hello，自定义锚点也算在内,#hello-6](#hello-6)

  <a href="#hello-6">raw-HTML跳转到第6次出现的hello</a>