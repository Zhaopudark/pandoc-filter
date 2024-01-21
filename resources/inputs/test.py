"""
Set all headers to level 1
"""
import pathlib
import panflute as pf
# from panflute import

def action(elem, doc):
    if isinstance(elem, Header):
        elem.level = 1

def main(doc=None):
    return run_filter(action, doc=doc) 

if __name__ == '__main__':

    with open("E:/Codes/Works/pandoc-filter/resources/inputs/test_md2md_figure.md", "r", encoding="utf-8") as f:
        markdown_content = f.read()
    doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
    pass
    print(doc.get_metadata())
    # if doc.get_metadata():
    #     doc.doc_path = file_path
    #     doc = main(doc,
    #                 oss_helper=oss_helper,
    #                 tracing_logger = tracing_logger,
    #                 global_abbrlink_file_recoder=global_abbrlink_file_recoder)
    #     with open(f"{target_dir}/{file_path.name}", "w", encoding="utf-8") as f:
    #         f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
      