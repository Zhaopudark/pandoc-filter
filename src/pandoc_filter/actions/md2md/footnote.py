import typeguard
import panflute as pf

from ...utils import TracingLogger

@typeguard.typechecked
def footnote_action(elem:pf.Element,doc:pf.Doc,**kwargs)->pf.Note|None: # Repleace
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    An action to process footnotes. Remove `\n` in the footnote content.
    """
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if isinstance(elem, pf.Note):
        tracing_logger.mark(elem)
        elem = pf.Note(pf.Para(pf.Str(pf.stringify(elem.content).strip(" \n"))))
        tracing_logger.check_and_log('footnote',elem)
        return elem