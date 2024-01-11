import pathlib
import logging
import functools
import panflute as pf

from pandoc_filter.utils import TracingLogger
from pandoc_filter.md2html_filters import anchor_filter,internal_link_recorder,link_like_filter
from pandoc_filter.md2md_filters import internal_link_filter

pathlib.Path("./logs").mkdir(parents=True, exist_ok=True)
tracing_logger = TracingLogger(name="./logs/pf_log",level=logging.INFO)

def _check_file_path(file_path:str)->pathlib.Path:
    file_path:pathlib.Path = pathlib.Path(file_path)
    assert file_path.exists()
    assert file_path.is_file()
    return file_path

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
    doc = pf.run_filter(action=internal_link_filter,doc=doc,tracing_logger=tracing_logger)
    _finalize = functools.partial(finalize,tracing_logger=tracing_logger)
    doc = pf.run_filters(actions=[anchor_filter,internal_link_recorder,link_like_filter],doc=doc,finalize=_finalize,tracing_logger=tracing_logger)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pf.convert_text(doc,input_format='panflute',output_format='html',standalone=True))