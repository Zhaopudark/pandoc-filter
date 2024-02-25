### Normalize internal link

- Inputs(`./input.md`): refer to [`test_md2md_internal_link.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/inputs/test_md2md_internal_link.md).

  ```markdown
  ## 带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格
  
  ### aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)
  
  [带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格](#####带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格)
  
  [aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)](#####aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy))
  
  <a href="###带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格">带空格 和`特殊字符`...</a>
  
  <a href="#aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)">aAa-b...</a>
  ```

- Coding:

  ```PowerShell
  pandoc ./input.md -o ./output.md -f markdown -t gfm -s --filter md2md-norm-internal-link-filter
  ```
  
- Outputs(`./output.md`): refer to [`test_md2md_internal_link.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/outputs/test_md2md_internal_link.md).

  ```markdown
  ## 带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试 空格
  
  ### aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz \[xx\] (yy)
  
  [带空格 和`特殊字符` \[链接\](http://typora.io) 用于%%%%￥￥￥￥跳转测试
  空格](#带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试 空格)
  
  [aAa-b cC `Dd`, a#%&\[xxx\](yyy) Zzz \[xx\]
  (yy)](#aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz \[xx\] (yy))
  
  <a href="#带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试 空格">带空格
  和`特殊字符`…</a>
  
  <a href="#aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz \[xx\] (yy)">aAa-b…</a>
  ```