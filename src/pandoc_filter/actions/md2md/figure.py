import typeguard
import pathlib
import panflute as pf

from ...utils import TracingLogger,OssHelper
from ...utils import get_html_src,sub_html_src

@typeguard.typechecked     
def figure_action(elem:pf.Element,doc:pf.Doc,doc_path:pathlib.Path,oss_helper:OssHelper,**kwargs)->None: # Modify In Place
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    An action to process images of local pictures when converting markdown to markdown.
    Manager local pictures, sync them to Aliyun OSS, and replace the original src with the new one.
    NOTE
        The argument `doc_path` and `oss_helper` should be given.
    """
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    
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