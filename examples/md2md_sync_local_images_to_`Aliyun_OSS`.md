# Sync local images to `Aliyun OSS`

- Prerequisites:

  - Consider the bucket domain is `raw.little-train.com`

  - Consider the environment variables have been given:

    - OSS_ENDPOINT_NAME = "oss-cn-taiwan.aliyuncs.com"
    - OSS_BUCKET_NAME = "test"
    - OSS_ACCESS_KEY_ID = "123456781234567812345678"

    - OSS_ACCESS_KEY_SECRET = "123456123456123456123456123456"

  - Consider images located in `./input.assets/`

- Inputs(`./input.md`): refer to [`test_md2md_figure.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/inputs/test_md2md_figure.md).

  ```markdown
  ![自定义头像](./input.assets/自定义头像.png)
  
  ![Level-of-concepts](./input.assets/Level-of-concepts.svg)
  ```

- Coding:

  ```python
  import pandoc_filter
  
  file_path = _check_file_path("./input.md")
  output_path = pathlib.Path(f"./output.md")
  answer_path = pathlib.Path(f"./resources/outputs/{file_path.name}")
  pandoc_filter.run_filters_pyio(
      file_path,output_path,'markdown','gfm',
      [pandoc_filter.md2md_upload_figure_to_aliyun_filter],doc_path=file_path)
  ```
  
- Outputs(`./output.md`): refer to [`test_md2md_figure.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/outputs/test_md2md_figure.md).

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