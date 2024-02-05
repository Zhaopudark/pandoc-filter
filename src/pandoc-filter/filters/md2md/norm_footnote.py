import typeguard
import panflute as pf

from ...utils import TracingLogger

r"""A pandoc filter that mainly for converting `markdown` to `markdown`.
Normalize the footnotes. Remove unnecessary `\n` in the footnote content.
"""


def _norm_footnote(elem:pf.Element,doc:pf.Doc,**kwargs)->pf.Note|None:
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    An action to process footnotes.
    Remove unnecessary `\n` in the footnote content.
    [replace elements]
    """
    typeguard.check_type(kwargs['tracing_logger'],TracingLogger)
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    
    if isinstance(elem, pf.Note):
        tracing_logger.mark(elem)
        elem = pf.Note(pf.Para(pf.Str(pf.stringify(elem.content).strip(" \n"))))
        tracing_logger.check_and_log('footnote',elem)
        return elem

def norm_footnote_filter(doc:pf.Doc=None,**kwargs):
    return pf.run_filters(actions=[_norm_footnote],doc=doc,tracing_logger=TracingLogger(),**kwargs)