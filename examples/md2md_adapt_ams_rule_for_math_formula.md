### Adapt AMS rule for math formula

- Inputs(`./input.md`): refer to [`test_md2md_math.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/inputs/test_md2md_math.md).

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

  ```PowerShell
  pandoc ./input.md -o ./output.md -f markdown -t gfm -s --filter md2md-enhance-equation-filter
  ```
  
- Outputs(`./output.md`): refer to [`test_md2md_math.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/outputs/test_md2md_math.md).

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