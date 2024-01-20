import logging
import typeguard
import panflute as pf

from ...utils import TracingLogger
from ...utils import check_pandoc_version

@typeguard.typechecked
def _footnote_filter(elem:pf.Element,doc:pf.Doc,**kwargs)->pf.Note|None: # Repleace
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to process footnotes. Remove `\n` in the footnote content.
    """
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if isinstance(elem, pf.Note):
        tracing_logger.mark(elem)
        elem = pf.Note(pf.Para(pf.Str(pf.stringify(elem.content).strip(" \n"))))
        tracing_logger.check_and_log('footnote',elem)
        return elem

def main(doc=None,**kwargs):
    check_pandoc_version(required_version='3.1.0')
    tracing_logger = TracingLogger(name='logs/pf_log',level=logging.WARNING)
    return pf.run_filters(
        actions=[_footnote_filter],
        doc=doc,
        tracing_logger=tracing_logger,
        **kwargs)