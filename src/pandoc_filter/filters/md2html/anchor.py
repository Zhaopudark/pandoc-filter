import re
import typeguard
import panflute as pf

from ...utils import TracingLogger
from ...utils import get_html_id,sub_html_id,get_text_hash

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

def anchor_filter(elem:pf.Element,doc,**kwargs)->None: # Modify In Place:
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to normalize anchors when converting markdown to html.
    """
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if not(hasattr(doc,'anchor_count') and isinstance(doc.anchor_count,dict)):
        doc.anchor_count = {}
    def _text_hash_count(text:str)->str:
        text_hash = get_text_hash(text)
        if text_hash in doc.anchor_count: # 按照text_hash值计数, 重复则加1
            doc.anchor_count[text_hash] += 1
        else:
            doc.anchor_count[text_hash] = 1
        return text_hash
    if isinstance(elem, pf.Header):
        tracing_logger.mark(elem)
        # 获取header文本内容并剔除#号
        header_text = pf.convert_text(elem,input_format='panflute',output_format='gfm',standalone=True).lstrip('#')
        text_hash = _text_hash_count(header_text)
        elem.identifier = f"{text_hash}-{doc.anchor_count[text_hash]}"
        tracing_logger.check_and_log('headings anchor',elem)
    elif isinstance(elem, pf.RawInline) and elem.format == 'html' and (raw_id_text:=get_html_id(elem.text)): # 获取id文本内容但不做任何剔除
        tracing_logger.mark(elem)
        text_hash = _text_hash_count(raw_id_text)
        elem.text = sub_html_id(elem.text,f"{text_hash}-{doc.anchor_count[text_hash]}")
        tracing_logger.check_and_log('raw-HTML anchor',elem)