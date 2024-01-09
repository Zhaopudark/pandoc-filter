- 带有特殊字符时，简化并改变了一般的Markdown渲染html的规则

  - 不遵从Typora的[internal-links](https://support.typoraio.cn/Links/#internal-links)语法
  - 直接将原内容复制到`[]()`的`()`内即可
  - 推荐使用上述方式，也只保证上述方式是可行的
  - 其余方式可能会出现意外结果

  ## 带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格

  ### aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  留白测试跳转

  - 使用markdown语法的链接到headings锚点
    - [带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格](#####带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格)
    - [aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)](#####aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy))
  - 使用raw-HTML链接到headings锚点
    - <a href="###带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格">带空格 和`特殊字符`...</a>
    - <a href="#aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)">aAa-b...</a>
