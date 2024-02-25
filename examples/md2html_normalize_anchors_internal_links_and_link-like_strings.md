### Normalize anchors, internal links and link-like strings

- Inputs(`./input.md`):

  Refer to [`test_md2html_anchor_and_link.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/inputs/test_md2html_anchor_and_link.md).

- Coding:

  ```powershell
  pandoc ./input.md -o ./output.html -f markdown -t html -s --filter md2md-norm-internal-link-filter --filtermd2html-hash-anchor-and-internal-link-filter --filter md2html-enhance-link-like-filter
  ```
  
- Outputs(`./output.html`):

  Refer to [`test_md2html_anchor_and_link.html`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/outputs/test_md2html_anchor_and_link.html).
