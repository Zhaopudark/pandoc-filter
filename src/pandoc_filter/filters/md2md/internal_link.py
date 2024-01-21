import logging
import typeguard
import urllib.parse
import panflute as pf

from ...utils import TracingLogger
from ...utils import get_html_href,sub_html_href

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

def _decode_internal_link_url(url:str)->str:
    r"""When converting markdown to any type via pandoc, md internal links' URLs may be automatically URL-encoded before any filter works.
    The encoding is done by default and may not be avoided.
    This function is used to decode the URL.
    """
    decoded_url = urllib.parse.unquote(url.lstrip('#'))
    header_mimic = pf.convert_text(f"# {decoded_url}",input_format='markdown',output_format='gfm',standalone=True)
    return f"#{header_mimic.lstrip('# ')}"

@typeguard.typechecked
def internal_link_filter(elem:pf.Element, doc:pf.Doc,**kwargs)->None: # Do not modify.
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to normalize internal links when converting markdown to markdown.
    """
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if isinstance(elem, pf.Link) and elem.url.startswith('#'):
        tracing_logger.mark(elem)       
        elem.url = _decode_internal_link_url(elem.url)
        tracing_logger.check_and_log('anchor_links',elem)
    elif isinstance(elem, pf.RawInline) and elem.format == 'html' and (old_href:=get_html_href(elem.text)) and old_href.startswith('#'):
        tracing_logger.mark(elem)
        elem.text = sub_html_href(elem.text,_decode_internal_link_url(old_href))
        tracing_logger.check_and_log('raw_anchor_links',elem)