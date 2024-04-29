# Pandoc-Filter 0.2.x

## Release 0.2.15
Working on...

## Release 0.2.14

- Modify `md2html_hash_anchor_and_internal_link_filter` to handle internal links within hexo tag plugins.
    - Now, it will compulsorily modify internal_link's url, even though its target is not found.

## Release 0.2.13
Add `md2html_increase_header_level_filter`, which will increase the header level by 1.
## Release 0.2.12
Remove more unnecessary type-checking clauses for accelerating.
## Release 0.2.11
Remove unnecessary type-checking for accelerating.
## Release 0.2.10
Fix bugs in `md2md_norm_footnote_filter` to avoid missing links in the footnote content.
## Release 0.2.9
Adjusted organization of README.md and RELEASE.md.
Examples were separated out.
## Release 0.2.8
Change logging modes in `md2md_convert_github_style_alert_to_hexo_style_alert_filter`.
## Release 0.2.7
Fix logging bugs in `md2md_convert_github_style_alert_to_hexo_style_alert_filter`.

## Release 0.2.6
Add `md2md_convert_github_style_alert_to_hexo_style_alert_filter`, which can convert the [github-style alert](https://github.com/orgs/community/discussions/16925) to hexo-style alert.The github-style alert is based on pandoc's `BlockQuote` element, while the hexo-style alert is based on [hexo tag plugins](https://hexo.io/docs/tag-plugins#Note).We use a general mode to confirm the hexo-style alert type, which are widely used in the hexo community by many themes, such as
- [hexo-theme-butterfly](https://butterfly.js.org/posts/4aa8abbe/?highlight=%25+endnote#%E6%A8%99%E7%B1%A4%E5%A4%96%E6%8E%9B%EF%BC%88Tag-Plugins%EF%BC%89),
- [hexo-theme-fluid](https://hexo.fluid-dev.com/docs/guide/#tag-%E6%8F%92%E4%BB%B6),
- [hexo-them-next](https://theme-next.js.org/docs/tag-plugins/note).
## Release 0.2.5
Re-organize the inner implementation about decoding url.

## Release 0.2.4
Fix a bug in `upload_figure_to_aliyun_filter` when local file path contains spaces.

## Release 0.2.3
Fix a bug in `run_filters_pyio` on invoking actions.

## Release 0.2.2
Add `**kwargs` to all filter functions for better compatibility.

## Release 0.2.1
Symplify `runtime_status_dict` to `runtime_dict`.

## Release 0.2.0
- Release 0.2.0.

## Release 0.2.0b1
- Add runtime status 

## Release 0.2.0b0
- Simplify APIs.
- Modify some helping scripts.
- Support command-line mode.

# Pandoc-Filter 0.1.0
## Release 0.1.0b1
Modify some helping scripts.

## Release 0.1.0b0
Begin to use semantic version control formally. For this project:
- We consider CI tests as alpha tests. So there is no alpha release.
- Use `z.y.0bn` as the pre-release (beta release) version number.
- Use `z.y.0` as the normal release version number.
- Use `z.y.n`, where `n > 0`, as the patch release version number.

# Pandoc-Filter 0.0.1
## Release 0.0.1
The first normal release.

## Release 0.0.1b2
Sync to Zenodo.

## Release 0.0.1b1
Add badges and other minor changes.

## Release 0.0.1b0
The first release of the project.