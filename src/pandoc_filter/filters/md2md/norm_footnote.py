import panflute as pf

from ...utils import TracingLogger

r"""A pandoc filter that mainly for converting `markdown` to `markdown`.
Normalize the footnotes. Remove unnecessary `\n` in the footnote content.
"""

def __deserialize_link_to_markdown(link:pf.Link)->str:
    return f"[{pf.stringify(link)}]({link.url})"

def _norm_footnote(elem:pf.Element,doc:pf.Doc,tracing_logger:TracingLogger,**kwargs)->pf.Note|None:
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    An action to process footnotes. Remove unnecessary `\n` in the footnote content.
    
    When converting `markdown` to `markdown`, if there is any pf.Space in pf.Note(pf.Para(...)), the 
    panflute/pandoc will layout elements and add `\n` to the content with some unkonwn rules.
    To remove the unnecessary `\n`, we need to aggregate words into a whole string, as this function does.
    
    [replace elements]
    """
    if isinstance(elem, pf.Note):
        tracing_logger.mark(elem)
        new_string = ""
        for para in elem.content:
            assert isinstance(para,pf.Para)
            for item in para.content:
                if isinstance(item,pf.Space):
                    new_string = new_string.strip(" \n") + " "
                elif isinstance(item,pf.Str):
                    new_string = new_string.strip(" \n") + " " + item.text.strip(" \n")
                elif isinstance(item,pf.Link):
                    new_string = new_string.strip(" \n") + " " + __deserialize_link_to_markdown(item).strip(" \n")
        elem = pf.Note(pf.Para(pf.Str(new_string)))
        tracing_logger.check_and_log('footnote',elem)
        return elem

def norm_footnote_filter(doc:pf.Doc=None,**kwargs):
    return pf.run_filters(actions=[_norm_footnote],doc=doc,tracing_logger=TracingLogger(),**kwargs)