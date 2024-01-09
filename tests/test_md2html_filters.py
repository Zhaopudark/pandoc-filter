import pathlib
import logging
import functools
import panflute as pf

from pandoc_filter.utils import TracingLogger
from pandoc_filter.utils import OssHelper
from pandoc_filter.md2html_filters import anchor_filter,internal_link_recorder,link_like_filter
from pandoc_filter.md2md_filters import math_filter,figure_filter,footnote_filter,internal_link_filter

pathlib.Path(f"./logs").mkdir(parents=True, exist_ok=True)
tracing_logger = TracingLogger(name=f"./logs/pf_log",level=logging.INFO)

def _check_file_path(file_path:str)->pathlib.Path:
    file_path:pathlib.Path = pathlib.Path(file_path)
    assert file_path.exists()
    assert file_path.is_file()
    return file_path

def _apply_md2md_filters(doc:pf.Doc,**kwargs):
    import os
    oss_endpoint_name = os.environ['OSS_ENDPOINT_NAME']
    oss_bucket_name = os.environ['OSS_BUCKET_NAME']
    assert os.environ['OSS_ACCESS_KEY_ID']
    assert os.environ['OSS_ACCESS_KEY_SECRET']
    oss_helper = OssHelper(oss_endpoint_name,oss_bucket_name)
    doc = pf.run_filters(actions=[math_filter,figure_filter,footnote_filter,internal_link_filter],doc=doc,oss_helper=oss_helper,**kwargs)
    return doc
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
    
def test_md2html_anchor_filter():
    file_path =_check_file_path("./resources/test_md2html_anchor_and_link.md")
    with open(file_path,'r',encoding='utf-8') as f:
        markdown_content = f.read()
    output_path = pathlib.Path(f"./temp/{file_path.stem}.html")
    doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
    doc = _apply_md2md_filters(doc,tracing_logger=tracing_logger)
    _finalize = functools.partial(finalize,tracing_logger=tracing_logger)
    doc = pf.run_filters(actions=[anchor_filter,internal_link_recorder,link_like_filter],doc=doc,finalize=_finalize,tracing_logger=tracing_logger)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pf.convert_text(doc,input_format='panflute',output_format='html',standalone=True))

      
# if __name__ == "__main__":
    
#     # 检查命令行参数是否包含文件名
#     if len(sys.argv) != 3:
#         print("Usage: python markdown_deployer.py <notes_dir> <target_dir>")
#         sys.exit(1)
#     print(sys.argv)
    
#     notes_dir = sys.argv[1]
#     target_dir = sys.argv[2]
    
#     import os
#     try:
#         oss_endpoint_name = os.environ['OSS_ENDPOINT_NAME']
#         oss_bucket_name = os.environ['OSS_BUCKET_NAME']
#         assert os.environ['OSS_ACCESS_KEY_ID']
#         assert os.environ['OSS_ACCESS_KEY_SECRET']
#     except KeyError as e:
#         print(f"Please set the environment variable {e}")
#         sys.exit(1)
    
#     oss_helper = OssHelper(oss_endpoint_name,oss_bucket_name)
#     global_abbrlink_file_recoder = {}
#     tracing_logger = TracingLogger(name='logs/pf_log',level=logging.WARNING)
#     logger = logger_factory(name='logs/pf_log',level=logging.WARNING)
#     for file_path in pathlib.Path(notes_dir).glob('**/*.md'):
#         try:
#             with open(file_path, "r", encoding="utf-8") as f:
#                 markdown_content = f.read()
#             doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
#             if doc.get_metadata():
#                 doc.doc_path = file_path
#                 doc = main(doc,
#                            oss_helper=oss_helper,
#                            tracing_logger = tracing_logger,
#                            global_abbrlink_file_recoder=global_abbrlink_file_recoder)
#                 with open(f"{target_dir}/{file_path.name}", "w", encoding="utf-8") as f:
#                     f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
#         except Exception as e:
#             logger.error(e)
#         finally:
#             f.close()
        