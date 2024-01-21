import os
import typeguard
import pathlib
import panflute as pf

from ...utils import TracingLogger,OssHelper
from ...utils import get_html_src,sub_html_src

@typeguard.typechecked     
def figure_filter(elem:pf.Element,doc:pf.Doc,**kwargs)->None: # Modify In Place
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to process images of local pictures when converting markdown to markdown.
    Manager local pictures, sync them to Aliyun OSS, and replace the original src with the new one.
    NOTE
        The `doc.doc_path` should be set before calling this filter.
        The `doc.doc_path` should be a pathlib.Path object.
        The local pictures should be within the same directory as the doc file.
    """
    oss_helper:OssHelper = kwargs['oss_helper']
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if not(hasattr(doc,'doc_path')):
        doc.doc_path = pathlib.Path(os.environ['CURRENT_DOC_PATH'])
    if not doc.doc_path.exists():
        tracing_logger.logger.warning(f"doc.doc_path {doc.doc_path} does not exist.")
        return None
    
    if isinstance(elem, pf.Image) and (old_src:=str(elem.url)).startswith('.'): # reletive path
        new_src = oss_helper.maybe_upload_file_and_get_src(doc.doc_path.parent/old_src)
        tracing_logger.mark(elem)
        elem.url = new_src
        tracing_logger.check_and_log('image',elem)
    elif isinstance(elem, pf.RawInline) and elem.format == 'html' and (old_src:=get_html_src(elem.text)) and old_src.startswith('.'): # reletive path
            new_src = oss_helper.maybe_upload_file_and_get_src(doc.doc_path.parent/old_src)
            tracing_logger.mark(elem)
            elem.text = sub_html_src(elem.text,new_src)
            tracing_logger.check_and_log('raw_html_img',elem)