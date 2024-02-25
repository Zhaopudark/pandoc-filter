# Normalize footnotes

- Inputs(`./input.md`): refer to [`test_md2md_footnote.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/inputs/test_md2md_footnote.md).

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

  ```powershell
  pandoc ./input.md -o ./output.md -f markdown -t gfm -s --filter md2md-norm-footnote-filter
  ```
  
- Outputs(`./output.md`): refer to [`test_md2md_footnote.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/outpts/test_md2md_footnote.md).

  ```markdown
  which1.[^1]
  
  which2.[^2]
  
  which3.[^3]
  
  [^1]: Deep Learning with Intel® AVX-512 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  
  [^2]: Deep Learning with Intel® AVX-512222 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  
  [^3]: Deep Learning with Intel® AVX-512 and Intel® DL Boost https://www.intel.cn/content/www/cn/zh/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html www.intel.cn
  ```
