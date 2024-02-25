<div align="center">
<strong>
<samp>

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pandoc-filter?logo=python)](https://badge.fury.io/py/pandoc-filter)
[![PyPI - Version](https://img.shields.io/pypi/v/pandoc-filter?logo=pypi)](https://pypi.org/project/pandoc-filter)
[![DOI](https://zenodo.org/badge/741871139.svg)](https://zenodo.org/doi/10.5281/zenodo.10528322)
[![GitHub License](https://img.shields.io/github/license/Zhaopudark/pandoc-filter)](https://github.com/Zhaopudark/pandoc-filter?tab=GPL-3.0-1-ov-file#readme)

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zhaopudark/pandoc-filter/test.yml?label=Test)](https://github.com/Zhaopudark/pandoc-filter/actions/workflows/test.yml)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zhaopudark/pandoc-filter/build_and_deploy.yml?event=release&label=Build%20and%20Deploy)](https://github.com/Zhaopudark/pandoc-filter/actions/workflows/build_and_deploy.yml)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zhaopudark/pandoc-filter/post_deploy_test.yml?event=workflow_run&label=End%20Test)](https://github.com/Zhaopudark/pandoc-filter/actions/workflows/post_deploy_test.yml)
[![codecov](https://codecov.io/gh/Zhaopudark/pandoc-filter/graph/badge.svg?token=lb3cLoh3e5)](https://codecov.io/gh/Zhaopudark/pandoc-filter)

</samp>
</strong>
</div>

# pandoc-filter

This project supports some useful and highly customized [pandoc python filters](https://pandoc.org/filters.html) that based on [panflute](http://scorreia.com/software/panflute/). They can meet some special requests when using [pandoc](https://pandoc.org) to

- [x] convert files from `markdown` to `gfm`
- [x] convert files from `markdown` to `html`
- [ ] convert other formats (In the future)

Please see [Main Features](#main-features) for the concrete features.

Please see [Samples](#Samples) for the recommend usage.

# Backgrounds

I'm used to taking notes with markdown and clean markdown syntax. Then, I usually post these notes on [my site](https://little-train.com/) as web pages. So, I need to convert markdown to html. There were many tools to achieve the converting and  I chose [pandoc](https://pandoc.org) at last due to its powerful features.

But sometimes, I need many more features when converting from `markdown` to `html`, where pandoc filters are needed. I have written some pandoc python filters with some advanced features by [panflute](https://github.com/sergiocorreia/panflute) and many other tools. And now, I think it's time to gather these filters into a combined toolset as this project. 

# Installation

```
pip install -i https://pypi.org/simple/ -U pandoc-filter
```

# Main Features

There are 2 supported ways:

-  **command-line-mode**: use non-parametric filters in command-lines with [pandoc](https://pandoc.org).
- **python-mode**: use `run_filters_pyio`  function in python.

For an example, `md2md_enhance_equation_filter` in [enhance_equation.py](https://github.com/Zhaopudark/pandoc-filter/blob/main/src/pandoc_filter/filters/md2md/enhance_equation.py) is a filter function as [panflute-user-guide ](http://scorreia.com/software/panflute/guide.html). And its registered command-line script is `md2md-enhance-equation-filter`. 

- So, after the installation, one can use it in **command-line-mode**:

  ```powershell
  pandoc ./input.md -o ./output.md -f markdown -t gfm -s --filter md2md-enhance-equation-filter
  ```

- Or, use in **python mode**

  ```python
  import pandoc_filter
  file_path = pathlib.Path("./input.md")
  output_path = pathlib.Path("./output.md")
  pandoc_filter.run_filters_pyio(file_path,output_path,'markdown','gfm',[pandoc_filter.md2md_enhance_equation_filter])
  ```

**Runtime status** can be recorded. In **python mode**, any filter function will return a proposed panflute `Doc`. Some filter functions will add an instance attribute dict `runtime_dict` to the returned `Doc`, as a record for **runtime status**, which may be very useful for advanced users.  For an example,  `md2md_enhance_equation_filter`, will add an instance attribute dict `runtime_dict` to the returned `Doc`, which may contain a mapping `{'math':True}` if there is any math element in the `Doc`.

All filters with corresponding  registered command-line scripts, the specific features, and the recorded **runtime status** are recorded in the following table:

> [!NOTE]
>
> Since some filters need additional arguments, not all filter functions support **command-line-mode**, even though they all support **python-mode** indeed.
>
> All filters support cascaded invoking.

| Filter Functions                                            | Command Line                                                | Additional Arguments | Features                                                     | Runtime status (`doc.runtime_dict`)                          |
| ----------------------------------------------------------- | ----------------------------------------------------------- | -------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
| md2md_convert_github_style_alert_to_hexo_style_alert_filter | md2md-convert-github-style-alert-to-hexo-style-alert-filter | -                    | Convert the [github-style alert](https://github.com/orgs/community/discussions/16925) to hexo-style alert. | -                                                            |
| md2md_enhance_equation_filter                               | md2md-enhance-equation-filter                               | -                    | Enhance math equations. Specifically, this filter will:  Adapt AMS rule for math formula.  Auto numbering markdown formulations within \begin{equation} \end{equation}, as in Typora. Allow multiple tags, but only take the first one. Allow multiple labels, but only take the first one. | {'math':< bool >,'equations_count':<some_number>}            |
| md2md_norm_footnote_filter                                  | md2md-norm-footnote-filter                                  | -                    | Normalize the footnotes. Remove unnecessary `\n` in the footnote content. | -                                                            |
| md2md_norm_internal_link_filter                             | md2md-norm-internal-link-filter                             | -                    | Normalize internal links' URLs. Decode the URL if it is URL-encoded. | -                                                            |
| md2md_upload_figure_to_aliyun_filter                        | -                                                           | doc_path             | Auto upload local pictures to Aliyun OSS. Replace the original `src` with the new one. The following environment variables should be given in advance:  `$Env:OSS_ENDPOINT_NAME`, `$Env:OSS_BUCKET_NAME`,  `$Env:OSS_ACCESS_KEY_ID` , and `$Env:OSS_ACCESS_KEY_SECRET`. The doc_path should be given in advance. | {'doc_path':<doc_path>,'oss_helper':<Oss_Helper>}            |
| md2html_centralize_figure_filter                            | md2html-centralize-figure-filter                            | -                    | ==Deprecated==                                               | -                                                            |
| md2html_enhance_link_like_filter                            | md2html-enhance-link-like-filter                            | -                    | Enhance the link-like string to a `link` element.            | -                                                            |
| md2html_hash_anchor_and_internal_link_filter                | md2html-hash-anchor-and-internal-link-filter                | -                    | Hash both the anchor's `id` and the internal-link's `url ` simultaneously. | {'anchor_count':<anchor_count_dict>,'internal_link_record':<internal_link_record_list>} |

# Samples

Here are 2 basic types of examples

## Convert markdown to markdown (Normalization)

- [Adapt AMS rule for math formula](https://github.com/Zhaopudark/pandoc-filter/blob/main/examples/md2md_adapt_ams_rule_for_math_formula.md)
- [Normalize footnotes](https://github.com/Zhaopudark/pandoc-filter/blob/main/examples/md2md_normalize_footnotes.md)
- [Normalize internal link](https://github.com/Zhaopudark/pandoc-filter/blob/main/examples/md2md_normalize_internal_link.md)
- [Sync local images to `Aliyun OSS`](https://github.com/Zhaopudark/pandoc-filter/blob/main/examples/md2md_sync_local_images_to_`Aliyun_OSS`.md)

## Convert markdown to html

- [Normalize anchors, internal links and link-like strings](https://github.com/Zhaopudark/pandoc-filter/blob/main/examples/md2html_normalize_anchors_internal_links_and_link-like_strings.md)


# Contribution

Contributions are welcome. But recently, the introduction and documentation are not complete. So, please wait for a while.

A simple way to contribute is to open an issue to report bugs or request new features.



