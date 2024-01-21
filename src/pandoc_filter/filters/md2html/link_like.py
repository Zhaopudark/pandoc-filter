import panflute as pf

from ...utils import TracingLogger

def link_like_filter(elem:pf.Element,doc:pf.Doc,**kwargs)->pf.Link|None: # Repleace
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to process a string that may be like a link. Replace the string with a `Link` element.
    """
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if isinstance(elem, pf.Str) and elem.text.lower().startswith('http'):
        tracing_logger.mark(elem)
        link = pf.Link(elem,url=elem.text)
        tracing_logger.check_and_log('link_like',elem)
        return link