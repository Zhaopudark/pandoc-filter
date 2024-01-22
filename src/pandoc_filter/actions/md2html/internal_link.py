import re
import typeguard
import panflute as pf

from ...utils import TracingLogger
from ...utils import get_html_href,sub_html_href,get_text_hash
from ..md2md.internal_link import _decode_internal_link_url

r"""Defination
In Markdown:
    anchors:
        headings anchors: `## aaa`
        raw-HTML anchors: `<a id="aaa"></a>`
    links:
        internal links:
            md internal links: `[bbb](#aaa)`
            raw-HTML internal links: `<a href="#aaa">bbb</a>`
        ...
    ...
"""        
class _PatchedInternalLink:
    @typeguard.typechecked
    def __init__(self,elem:pf.Link) -> None:
        self.elem = elem
    @typeguard.typechecked
    def sub(self,url:str,tracing_logger:TracingLogger)->None:
        tracing_logger.mark(self.elem)
        self.elem.url = f"#{url}"
        tracing_logger.check_and_log('internal_link',self.elem)

class _PatchedInternalRawLink:
    @typeguard.typechecked
    def __init__(self,elem:pf.RawInline) -> None:
        self.elem = elem
    @typeguard.typechecked
    def sub(self,url:str,tracing_logger:TracingLogger)->None:
        tracing_logger.mark(self.elem)
        self.elem.text = sub_html_href(self.elem.text,f"#{url}")   
        tracing_logger.check_and_log('internal_link',self.elem)

def internal_link_recorder(elem:pf.Element, doc:pf.Doc,**kwargs)->None: # Do not modify.
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A recorder to pre-normalize and record internal links when converting markdown to html.
    Since internal links should match anchors, if we want to normalize internal links better, we should consider global information comprehensively.
    So, the modification on internal links should be performed at the global level but not the node level as here.
    """
    if not(hasattr(doc,'internal_link_record') and isinstance(doc.internal_link_record,list)):
        doc.internal_link_record = []
    def _url_hash_guess(text:str)->str:
        old_url = text.lstrip('#')
        url = get_text_hash(old_url)
        if match:= re.search(r'-(?P<guessed_index>\d+)$', old_url):
            guessed_index = int(match.groupdict()['guessed_index'])  # 从匹配结果中提取数字部分
            if guessed_index == 0:
                guessed_index = 1
            url_striped = old_url[:match.start()]  # 从匹配结果中提取数字前面的部分
            guessed_url_with_num = get_text_hash(url_striped) + f"-{guessed_index}"
        else:
            guessed_url_with_num = None
        return url,guessed_url_with_num
      
    if isinstance(elem, pf.Link) and elem.url.startswith('#'):
        # Olny md internal links need to be decoded since it will be encoded by pandoc before filter.
        decoded_url = _decode_internal_link_url(elem.url) 
        url,guessed_url_with_num = _url_hash_guess(decoded_url)
        doc.internal_link_record.append((_PatchedInternalLink(elem),url,guessed_url_with_num))
    elif isinstance(elem, pf.RawInline) and elem.format == 'html' and (old_href:=get_html_href(elem.text)) and old_href.startswith('#'):
        # raw-HTML internal links will not be encoded by pandoc before filter. So there is no need to decode it.
        url,guessed_url_with_num = _url_hash_guess(old_href)
        doc.internal_link_record.append((_PatchedInternalRawLink(elem),url,guessed_url_with_num))