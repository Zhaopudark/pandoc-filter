# Convert github-style alert to hexo-style alert

- Inputs(`./input.md`): refer to [`test_md2md_alert.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/inputs/test_md2md_alert.md).

  ```markdown
  > [!NOTE]  
  > Highlights information that users should take into account, even when skimming.
  
  > [!TIP]
  > Optional information to help a user be more successful.
  
  > [!IMPORTANT]  
  > Crucial information necessary for users to succeed.
  
  > [!WARNING]  
  > Critical content demanding immediate user attention due to potential risks.
  
  > [!CAUTION]
  > Negative potential consequences of an action.


  > !NOTE 
  > Highlights information that users should take into account, even when skimming.



  - Note

    > [!Note]
    >
    > Highlights information that users should take into account, even when skimming.

    - Tip

      > [!tip]
      >
      > Optional information to help a user be more successful.

      - Important

        > [!important]
        >
        > Crucial information necessary for users to succeed.

        - Warning

          > [!warning]
          >
          > Critical content demanding immediate user attention due to potential risks.

          - Caution

            > [!caution]
            >
            > Negative potential consequences of an action.

- Coding:

  ```powershell
  pandoc ./input.md -o ./output.md -f markdown -t gfm -s --filter md2md-convert-github-style-alert-to-hexo-style-alert-filter
  ```

- Outputs(`./output.md`): refer to [`test_md2md_alert.md`](https://github.com/Zhaopudark/pandoc-filter/blob/main/resources/outputs/test_md2md_alert.md).

  ```markdown
  {% note info %}
  
  Highlights information that users should take into account, even when
  skimming.
  
  {% endnote %}
  
  {% note success %}
  
  Optional information to help a user be more successful.
  
  {% endnote %}
  
  {% note primary %}
  
  Crucial information necessary for users to succeed.
  
  {% endnote %}
  
  {% note warning %}
  
  Critical content demanding immediate user attention due to potential
  risks.
  
  {% endnote %}
  
  {% note danger %}
  
  Negative potential consequences of an action.
  
  {% endnote %}
  
  > !NOTE Highlights information that users should take into account, even
  > when skimming.
  
  - Note
  
    {% note info %}
  
    Highlights information that users should take into account, even when
    skimming.
  
    {% endnote %}
  
    - Tip
  
      {% note success %}
  
      Optional information to help a user be more successful.
  
      {% endnote %}
  
      - Important
  
        {% note primary %}
  
        Crucial information necessary for users to succeed.
  
        {% endnote %}
  
        - Warning
  
          {% note warning %}
  
          Critical content demanding immediate user attention due to
          potential risks.
  
          {% endnote %}
  
          - Caution
  
            {% note danger %}
  
            Negative potential consequences of an action.
  
            {% endnote %}
  ```