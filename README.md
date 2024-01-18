<div align="center">
<strong>
<samp>

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pandoc-filter)](https://badge.fury.io/py/pandoc-filter)
[![PyPI - Version](https://img.shields.io/pypi/v/pandoc-filter)](https://pypi.org/project/pandoc-filter)
[![DOI](https://zenodo.org/badge/741871139.svg)](https://zenodo.org/doi/10.5281/zenodo.10528322)
[![GitHub License](https://img.shields.io/github/license/Zhaopudark/pandoc-filter)](https://github.com/Zhaopudark/pandoc-filter?tab=GPL-3.0-1-ov-file#readme)</samp>

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zhaopudark/pandoc-filter/local_test.yml?label=Local%20Test)](https://github.com/Zhaopudark/pandoc-filter/actions/workflows/local_test.yml)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zhaopudark/pandoc-filter/build_and_deploy.yml?label=Build)](https://github.com/Zhaopudark/pandoc-filter/actions/workflows/build_and_deploy.yml)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zhaopudark/pandoc-filter/post_deploy_test.yml?label=Test)](https://github.com/Zhaopudark/pandoc-filter/actions/workflows/post_deploy_test.yml)
[![codecov](https://codecov.io/gh/Zhaopudark/pandoc-filter/graph/badge.svg?token=lb3cLoh3e5)](https://codecov.io/gh/Zhaopudark/pandoc-filter)
</strong>
</div>




# pandoc-filter

This project is a customized [pandoc](https://pandoc.org) filters set that can be used to generate a useful [pandoc python filter](https://pandoc.org/filters.html). Recently, it only supports some features of `markdown-to-markdown` (normalizing markdown files) and `markdown-to-html` (generating web pages). But more features will be added later as my scenario and the user's feedback.

# Backgrounds

I'm used to taking notes with markdown and clean markdown syntax. Then, I usually post these notes on [my site](https://little-train.com/) as web pages. So, I need to convert markdown to html. There were many tools to achieve the converting and  I chose [pandoc](https://pandoc.org) at last due to its powerful features.

But sometimes, I need many more features when converting from `md` to `html`, where pandoc filters are needed. I have written some pandoc python filters with some advanced features by [panflute](https://github.com/sergiocorreia/panflute) and many other tools. And now, I think it's time to gather these filters into a combined toolset as this project. 

Please see [Main Features](#main-features) for the concrete features.

Please see [Usage](#usage) for the recommend usage.

## Main Features

Mainly for converting markdown to html, I divided this process into two processes, i.e., `markdown-to-markdown` (normalizing markdown files) and `markdown-to-html` (generating web pages).

- `markdown-to-markdown` supports:
  - [x] math filter
    - [x]  Adapt AMS rule for math formula. (Auto numbering markdown formulations within `\begin{equation} \end{equation}`, as in Typora)
    - [x] Allow multiple tags, but only take the first one.
    - [x] Allow multiple labels, but only take the first one.
  - [x] figure filter
    - [x] Manager local pictures, sync them to `Aliyun OSS`, and replace the original `src` with the new one.
  - [x] footnote filter
    - [x] Normalize footnotes. (Remove `\n` in the footnote content.)
  - [x] internal link filter
    - [x] Normalize internal links with a very special rule. (Decode the URL-encoded links)
- `markdown-to-html`
  - [x] anchor filter
    - [x] Normalize anchors with a very special rule. (replace its `id` with its `hash` as [Notion](https://www.notion.so/) does, and numbering it with `-x`)
  - [x] internal link recorder and filter
    - [x] Globally manage and normalize internal links. (Make it match the behavior of `anchor filter`)
  - [x] link like filter
    - [x] Process a string that may be like a link. (Make it a link)

Note: The division of filters is just my opinion on code organization, it doesn't mean they can only be used for a certain class. As long as the user understands the effect of the filter, all filters are not restricted to use in any scenario. So, it is recommended to read a filter's [source codes](https://github.com/Zhaopudark/pandoc-filter) directly when using it.

# Installation

```
pip install -i https://pypi.org/simple/ --pre -U pandoc-filter
```

# Usage

Here are 2 basic examples

## Convert markdown to markdown (Normalization)

Normalize internal link

- Inputs(`./input.md`): refer to [`test_md2md_internal_link.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/test_md2md_internal_link.md).

  ```markdown
  ## 带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格
  
  ### aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)
  
  [带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格](#####带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格)
  
  [aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)](#####aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy))
  
  <a href="###带空格 和`特殊字符` [链接](http://typora.io) 用于%%%%￥￥￥￥跳转测试        空格">带空格 和`特殊字符`...</a>
  
  <a href="#aAa-b cC `Dd`, a#%&[xxx](yyy) Zzz [xx]  (yy)">aAa-b...</a>
  ```

- Coding:

  ```python
  import pathlib
  import logging
  import panflute as pf
  
  from pandoc_filter.utils import TracingLogger
  from pandoc_filter.md2md_filters import internal_link_filter
  
  pathlib.Path("./logs").mkdir(parents=True, exist_ok=True)
  tracing_logger = TracingLogger(name="./logs/pf_log",level=logging.INFO)
  
  file_path = pathlib.Path("./input.md")
  with open(file_path,'r',encoding='utf-8') as f:
      markdown_content = f.read()
  output_path = pathlib.Path("./output.md")
  
  doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
  doc = pf.run_filter(action=internal_link_filter,doc=doc,tracing_logger=tracing_logger)
  
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
  ```

- Outputs(`./output.md`): refer to [`test_md2md_internal_link.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/temp/test_md2md_internal_link.md).

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

### Normalize footnotes

- Inputs(`./input.md`): refer to [`test_md2md_footnote.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/test_md2md_footnote.md).

  ```markdown
  which1.[^1]
  
  which2.[^2]
  
  which3.[^3]
  
  [^1]: Deep Learning with Intel® AVX-512 and Intel® DL Boost
  https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html
  www.intel.cn
  
  [^2]: Deep Learning with Intel® AVX-512222 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  
  [^3]: Deep Learning with Intel®     AVX-512 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  ```

- Coding:

  ```python
  import pathlib
  import logging
  import panflute as pf
  
  from pandoc_filter.utils import TracingLogger
  from pandoc_filter.md2md_filters import footnote_filter
  
  pathlib.Path("./logs").mkdir(parents=True, exist_ok=True)
  tracing_logger = TracingLogger(name="./logs/pf_log",level=logging.INFO)
  
  file_path = pathlib.Path("./input.md")
  with open(file_path,'r',encoding='utf-8') as f:
      markdown_content = f.read()
  output_path = pathlib.Path("./output.md")
  
  doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
  doc = pf.run_filter(action=footnote_filter,doc=doc,tracing_logger=tracing_logger)
  
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
  ```

- Outputs(`./output.md`): refer to [`test_md2md_footnote.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/temp/test_md2md_footnote.md).

  ```markdown
  which1.[^1]
  
  which2.[^2]
  
  which3.[^3]
  
  [^1]: Deep Learning with Intel® AVX-512 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  
  [^2]: Deep Learning with Intel® AVX-512222 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  
  [^3]: Deep Learning with Intel® AVX-512 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  ```

### Adapt AMS rule for math formula

- Inputs(`./input.md`): refer to [`test_md2md_math.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/test_md2md_math.md).

  ```markdown
  $$
  \begin{equation}\tag{abcd}\label{lalla}
  e=mc^2
  \end{equation}
  $$
  
  $$
  \begin{equation}
  e=mc^2
  \end{equation}
  $$
  
  $$
  e=mc^2
  $$
  
  $$
  \begin{equation}\label{eq1}
  e=mc^2
  \end{equation}
  $$
  ```

- Coding:

  ```python
  import pathlib
  import logging
  import panflute as pf
  
  from pandoc_filter.utils import TracingLogger
  from pandoc_filter.md2md_filters import math_filter
  
  
  pathlib.Path("./logs").mkdir(parents=True, exist_ok=True)
  tracing_logger = TracingLogger(name="./logs/pf_log",level=logging.INFO)
  
  file_path = pathlib.Path("./input.md")
  with open(file_path,'r',encoding='utf-8') as f:
      markdown_content = f.read()
  output_path = pathlib.Path("./output.md")
  
  doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
  doc = pf.run_filter(action=math_filter,doc=doc,tracing_logger=tracing_logger)
  
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
  ```

- Outputs(`./output.md`): refer to [`test_md2md_math.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/temp/test_md2md_math.md).

  ```markdown
  $$
  \begin{equation}\label{lalla}\tag{abcd}
  e=mc^2
  \end{equation}
  $$
  
  $$
  \begin{equation}\tag{1}
  e=mc^2
  \end{equation}
  $$
  
  $$
  e=mc^2
  $$
  
  $$
  \begin{equation}\label{eq1}\tag{2}
  e=mc^2
  \end{equation}
  $$
  ```

### Sync local images to `Aliyun OSS`

- Prerequisites:

  - Consider the bucket domain is `raw.little-train.com`

  - Consider the environment variables have been given:

    - OSS_ENDPOINT_NAME = "oss-cn-taiwan.aliyuncs.com"
    - OSS_BUCKET_NAME = "test"
    - OSS_ACCESS_KEY_ID = "123456781234567812345678"

    - OSS_ACCESS_KEY_SECRET = "123456123456123456123456123456"

  - Consider images located in `./input.assets/`

- Inputs(`./input.md`): refer to [`test_md2md_figure.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/test_md2md_figure.md).

  ```markdown
  ![自定义头像](./input.assets/自定义头像.png)
  
  ![Level-of-concepts](./input.assets/Level-of-concepts.svg)
  ```

- Coding:

  ```python
  import pathlib
  import logging
  import panflute as pf
  
  from pandoc_filter.utils import TracingLogger
  from pandoc_filter.utils import OssHelper
  from pandoc_filter.md2md_filters import figure_filter
  
  pathlib.Path("./logs").mkdir(parents=True, exist_ok=True)
  tracing_logger = TracingLogger(name="./logs/pf_log",level=logging.INFO)
  
  file_path = pathlib.Path("./input.md")
  with open(file_path,'r',encoding='utf-8') as f:
      markdown_content = f.read()
  output_path = pathlib.Path("./output.md")
  
  import os
  oss_endpoint_name = os.environ['OSS_ENDPOINT_NAME']
  oss_bucket_name = os.environ['OSS_BUCKET_NAME']
  assert os.environ['OSS_ACCESS_KEY_ID']
  assert os.environ['OSS_ACCESS_KEY_SECRET']
  oss_helper = OssHelper(oss_endpoint_name,oss_bucket_name)
  
  doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
  doc.doc_path = file_path
  doc = pf.run_filter(action=figure_filter,doc=doc,tracing_logger=tracing_logger,oss_helper=oss_helper)
  
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
  ```

- Outputs(`./output.md`): refer to [`test_md2md_figure.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/temp/test_md2md_figure.md).

  ```markdown
  <figure>
  <img
  src="https://raw.little-train.com/111199e36daf608352089b12cec935fc5cbda5e3dcba395026d0b8751a013d1d.png"
  alt="自定义头像" />
  <figcaption aria-hidden="true">自定义头像</figcaption>
  </figure>
  
  <figure>
  <img
  src="https://raw.little-train.com/20061af9ba13d3b92969dc615b9ba91abb4c32c695f532a70a6159d7b806241c.svg"
  alt="Level-of-concepts" />
  <figcaption aria-hidden="true">Level-of-concepts</figcaption>
  </figure>
  ```

## Convert markdown to html

### Normalize anchors, internal links and link-like strings

- Inputs(`./input.md`):

  Refer to [`test_md2html_anchor_and_link.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/test_md2html_anchor_and_link.md).

- Coding:

  ```python
  import pathlib
  import logging
  import functools
  import panflute as pf
  
  from pandoc_filter.utils import TracingLogger
  from pandoc_filter.md2html_filters import anchor_filter,internal_link_recorder,link_like_filter
  from pandoc_filter.md2md_filters import internal_link_filter
  
  pathlib.Path(f"./logs").mkdir(parents=True, exist_ok=True)
  tracing_logger = TracingLogger(name="./logs/pf_log",level=logging.INFO)
  
  def finalize(doc:pf.Doc,**kwargs):
      tracing_logger = kwargs['tracing_logger']
      id_set = set()
      for k,v in doc.anchor_count.items():
          for i in range(1,v+1):
              id_set.add(f"{k}-{i}")
      for patched_elem,url,guessed_url_with_num in doc.internal_link_record:
          if f"{url}-1" in id_set:
              patched_elem.sub(f"{url}-1",tracing_logger)
          elif guessed_url_with_num in id_set: # None is not in id_set
              patched_elem.sub(f"{guessed_url_with_num}",tracing_logger)
          else:
              tracing_logger.logger.warning(f"{patched_elem.elem}")
              tracing_logger.logger.warning(f"The internal link `{url}` is invalid and will not be changed because no target header is found.")
  
  file_path = pathlib.Path("./input.md")
  with open(file_path,'r',encoding='utf-8') as f:
      markdown_content = f.read()
  output_path = pathlib.Path("./output.html")
  
  doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
  doc = pf.run_filter(action=internal_link_filter,doc=doc,tracing_logger=tracing_logger)
  
  _finalize = functools.partial(finalize,tracing_logger=tracing_logger)
  doc = pf.run_filters(actions=[anchor_filter,internal_link_recorder,link_like_filter],doc=doc,finalize=_finalize,tracing_logger=tracing_logger)
  
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(pf.convert_text(doc,input_format='panflute',output_format='html',standalone=True))
  ```

- Outputs(`./output.html`):

  Refer to [`test_md2html_anchor_and_link.html`](https://github.com/Zhaopudark/pandoc-filter/blob/main/temp/test_md2html_anchor_and_link.html).

# Contribution

Contributions are welcome. But recently, the introduction and documentation are not complete. So, please wait for a while.

A simple way to contribute is to open an issue to report bugs or request new features.



