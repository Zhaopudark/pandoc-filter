__version__ = '0.1.0b1'

import functools
import os
import logging
import panflute as pf

from .utils import TracingLogger,OssHelper
from .utils import check_pandoc_version

from .filters import md2md
from .filters import md2html

def pandoc_filer_wrapper(func):
    @functools.wraps(func)
    def wrapper(doc=None,**kwargs):
        check_pandoc_version(required_version='3.1.0')
        tracing_logger:TracingLogger = TracingLogger(name='logs/pf_log',level=logging.WARNING)
        return func(doc,tracing_logger=tracing_logger,**kwargs)
    return wrapper

## md2md
@pandoc_filer_wrapper
def md2md_figure_filter(doc=None,**kwargs):
    oss_endpoint_name = os.environ['OSS_ENDPOINT_NAME']
    oss_bucket_name = os.environ['OSS_BUCKET_NAME']
    assert os.environ['OSS_ACCESS_KEY_ID']
    assert os.environ['OSS_ACCESS_KEY_SECRET']
    oss_helper = OssHelper(oss_endpoint_name,oss_bucket_name)
    return pf.run_filters(actions=[md2md.figure.figure_filter],doc=doc,oss_helper=oss_helper,**kwargs)

@pandoc_filer_wrapper
def md2md_footnote_filter(doc=None,**kwargs):
    return pf.run_filters(actions=[md2md.footnote.footnote_filter],doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2md_internal_link_filter(doc=None,**kwargs):
    return pf.run_filters(actions=[md2md.internal_link.internal_link_filter],doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2md_math_filter(doc=None,**kwargs):
    return pf.run_filters(actions=[md2md.math.math_filter],doc=doc,**kwargs)

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
            md2html.anchor.anchor_filter,
            md2html.internal_link.internal_link_recorder],
        finalize=_finalize,
        doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2html_figure_filter(doc=None,**kwargs):
    return pf.run_filters(actions= [md2html.figure.figure_filter],doc=doc,**kwargs)

@pandoc_filer_wrapper
def md2html_link_like_filter(doc=None,**kwargs):
    return pf.run_filters(actions= [md2html.link_like.link_like_filter],doc=doc,**kwargs)