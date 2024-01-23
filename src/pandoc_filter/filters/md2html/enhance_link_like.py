import typeguard
import panflute as pf

from ...utils import TracingLogger

r"""A pandoc filter that mainly for converting `markdown` to `html`.
Enhance the link-like string to a `link` element.
"""


def _enhance_link_like(elem:pf.Element,doc:pf.Doc)->pf.Link|None:
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    An action to process a string that may be like a link.
    Replace the string with a `Link` element.
    [replace elements]
    """
    tracing_logger = TracingLogger()
    if isinstance(elem, pf.Str) and elem.text.lower().startswith('http'):
        tracing_logger.mark(elem)
        link = pf.Link(elem,url=elem.text)
        tracing_logger.check_and_log('link_like',elem)
        return link

def enhance_link_like_filter(doc:pf.Doc=None)->pf.Doc:
    return pf.run_filters(actions=[_enhance_link_like],doc=doc)

