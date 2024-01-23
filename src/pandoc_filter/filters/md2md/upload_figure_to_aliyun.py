import os
import functools
import pathlib

import typeguard
import panflute as pf

from ...utils import TracingLogger,OssHelper
from ...utils import get_html_src,sub_html_src

r"""A pandoc filter that mainly for converting `markdown` to `markdown`.
Auto upload local pictures to Aliyun OSS. Replace the original `src` with the new one.

NOTE:
    The following environment variables should be given in advance:
        $Env:OSS_ENDPOINT_NAME
        $Env:OSS_BUCKET_NAME
        $Env:OSS_ACCESS_KEY_ID
        $Env:OSS_ACCESS_KEY_SECRET
    The doc_path should be given in advance.
"""

@typeguard.typechecked
def _prepare_upload_figure_to_aliyun(doc:pf.Doc,*,doc_path:pathlib.Path)->None: 
    assert doc_path.exists(),f"doc_path: {doc_path} does not exist."
    assert os.environ['OSS_ENDPOINT_NAME'], "OSS_ENDPOINT_NAME is not given in environment variables."
    assert os.environ['OSS_BUCKET_NAME'], "OSS_BUCKET_NAME is not given in environment variables."
    assert os.environ['OSS_ACCESS_KEY_ID'], "OSS_ACCESS_KEY_ID is not given in environment variables."
    assert os.environ['OSS_ACCESS_KEY_SECRET'], "OSS_ACCESS_KEY_SECRET is not given in environment variables."
    doc.doc_path = doc_path
    doc.oss_helper = OssHelper(os.environ['OSS_ENDPOINT_NAME'],os.environ['OSS_BUCKET_NAME'])

def _upload_figure_to_aliyun(elem:pf.Element,doc:pf.Doc)->None:
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    An `action` function to upload local pictures to Aliyun OSS. Replace the original src with the new one.
    [modify elements in place]
    """
    tracing_logger = TracingLogger()
    oss_helper: OssHelper = doc.oss_helper
    doc_path: pathlib.Path = doc.doc_path
    if isinstance(elem, pf.Image) and (old_src:=str(elem.url)).startswith('.'): # reletive path
        new_src = oss_helper.maybe_upload_file_and_get_src(doc_path.parent/old_src)
        tracing_logger.mark(elem)
        elem.url = new_src
        tracing_logger.check_and_log('image',elem)
    elif isinstance(elem, pf.RawInline) and elem.format == 'html' and (old_src:=get_html_src(elem.text)) and old_src.startswith('.'): # reletive path
            new_src = oss_helper.maybe_upload_file_and_get_src(doc_path.parent/old_src)
            tracing_logger.mark(elem)
            elem.text = sub_html_src(elem.text,new_src)
            tracing_logger.check_and_log('raw_html_img',elem)

def _finalize_upload_figure_to_aliyun(doc:pf.Doc)->None:
    del doc.doc_path
    del doc.oss_helper
  
@typeguard.typechecked
def upload_figure_to_aliyun_filter(doc:pf.Doc=None,doc_path:pathlib.Path=None):
    __prepare_upload_figure_to_aliyun = functools.partial(_prepare_upload_figure_to_aliyun,doc_path=doc_path)
    return pf.run_filters(
        actions=[_upload_figure_to_aliyun],
        prepare=__prepare_upload_figure_to_aliyun,
        finalize=_finalize_upload_figure_to_aliyun,
        doc=doc)