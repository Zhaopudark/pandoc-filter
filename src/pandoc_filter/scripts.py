import functools
import pathlib
import os
import logging
from typing import Callable
import panflute as pf
import typeguard

from .utils import TracingLogger,OssHelper
from .utils import check_pandoc_version

from .actions import md2md
from .actions import md2html

def pandoc_filer_wrapper(func):
    @functools.wraps(func)
    def wrapper(doc=None,**kwargs):
        check_pandoc_version(required_version='3.1.0')
        tracing_logger:TracingLogger = TracingLogger(name='logs/pf_log',level=logging.WARNING)
        return func(doc=doc,tracing_logger=tracing_logger,**kwargs)
    return wrapper

@typeguard.typechecked
def run_filters_pyio(input_path:pathlib.Path,
                     output_path:pathlib.Path,
                     input_format:str,
                     output_format:str,
                     actions:list[Callable],
                     prepare:Callable|None=None,
                     finalize:Callable|None=None,
                     doc:pf.Doc|None=None,
                     **kwargs):
    with open(input_path, "r", encoding='utf-8') as f:
        markdown_content = f.read()
    doc = pf.convert_text(markdown_content,input_format=input_format,output_format='panflute',standalone=True)
    if prepare:
        doc = prepare(doc,**kwargs)
    for action in actions:
        doc = action(doc,**kwargs)
    if finalize:
        doc = finalize(doc,**kwargs)
    with open(output_path, "w", encoding="utf-8") as f:
        text = pf.convert_text(doc,input_format='panflute',output_format=output_format,standalone=True)
        if not text.endswith('\n'):
            text += '\n'
        f.write(text) 

## md2md
@pandoc_filer_wrapper
@typeguard.typechecked
def md2md_figure_filter(*,doc_path,doc=None,**kwargs):
    assert doc_path.exists(),f"doc_path: {doc_path} does not exist."
    
    oss_endpoint_name = os.environ['OSS_ENDPOINT_NAME']
    oss_bucket_name = os.environ['OSS_BUCKET_NAME']
    assert os.environ['OSS_ACCESS_KEY_ID']
    assert os.environ['OSS_ACCESS_KEY_SECRET']
    figure_filter = functools.partial(md2md.figure.figure_action,
                                      doc_path=doc_path,
                                      oss_helper = OssHelper(oss_endpoint_name,oss_bucket_name))
    return pf.run_filters(actions=[figure_filter],doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2md_footnote_filter(doc=None,**kwargs):
    return pf.run_filters(actions=[md2md.footnote.footnote_action],doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2md_internal_link_filter(doc=None,**kwargs):
    return pf.run_filters(actions=[md2md.internal_link.internal_link_action],doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2md_math_filter(doc=None,**kwargs):
    return pf.run_filters(actions=[md2md.math.math_action],doc=doc,**kwargs)

## md2html
@pandoc_filer_wrapper
def md2html_anchor_and_internal_link_filter(doc=None,**kwargs):
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
    _finalize = functools.partial(finalize,**kwargs)
    return pf.run_filters(
        actions= [
            md2html.anchor.anchor_action,
            md2html.internal_link.internal_link_recorder],
        finalize=_finalize,
        doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2html_figure_filter(doc=None,**kwargs):
    return pf.run_filters(actions= [md2html.figure.figure_action],doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2html_link_like_filter(doc=None,**kwargs):
    return pf.run_filters(actions= [md2html.link_like.link_like_action],doc=doc,**kwargs)