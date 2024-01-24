import re
import typeguard
import panflute as pf

from ...utils import TracingLogger,RuntimeStatusDict

r"""A pandoc filter that mainly for converting `markdown` to `markdown`.
Enhance math equations.
Specifically, this filter will:
    - Adapt AMS rule for math formula.
        - Auto numbering markdown formulations within \begin{equation} \end{equation}, as in Typora.
    - Allow multiple tags, but only take the first one.
    - Allow multiple labels, but only take the first one.
"""

def _prepare_enhance_equation(doc:pf.Doc)->None:
    doc.runtime_status_dict = RuntimeStatusDict(
        {'math':False,
        'equations_count':0})

@typeguard.typechecked
def _enhance_equation(elem:pf.Element,doc:pf.Doc)->None:
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    An action to enhance math equations.
    [modify elements in place]
    
    To make equations recognized correctly, 
        content like the following irregular syntax should to be avoided (unnecessary line breaks):
    ```markdown
    \begin{equation}\tag{33124124}
    e=mc^2 \\
    e=mc^2 \\

    \begin{aligned}
    \\
    \\
    \\
    e=mc^2 \\
    e=mc^2 \\
    \end{aligned}
    \end{equation}
    ```
    """
    tracing_logger = TracingLogger()
    if isinstance(elem, pf.elements.Math):
        doc.runtime_status_dict.lazy_update(key='math',value=True)
        if elem.format == "DisplayMath":
            tracing_logger.mark(elem)
            text = elem.text
            # delete all labels and tags but record the first one
            first_label = ''
            if matched:= re.search(r"(\\label{[^{}]*})",text): 
                first_label = matched.group(0)
                text = re.sub(r"(\\label{[^{}]*})",'',text)
            first_tag = ''
            if matched:= re.search(r"(\\tag{[^{}]*})",text): 
                first_tag = matched.group(0)
                text = re.sub(r"(\\tag{[^{}]*})",'',text)
            
            if (re.search(r"^\s*\\begin{equation}",text) and re.search(r"\\end{equation}\s*$",text)):
                text = re.sub(r"^\s*\\begin{equation}",'',text)
                text = re.sub(r"\\end{equation}\s*$",'',text)
                
                if first_tag != '':
                    text = f"\\begin{{equation}}{first_label}{first_tag}\n{text.strip(" \n")}\n\\end{{equation}}"
                else:
                    doc.runtime_status_dict['equations_count'] += 1
                    text = f"\\begin{{equation}}{first_label}\\tag{{{doc.runtime_status_dict['equations_count']}}}\n{text.strip(" \n")}\n\\end{{equation}}"
            else:
                text = f"{text}\n{first_label}{first_tag}"
            elem.text = f"\n{text.strip(" \n")}\n"
            tracing_logger.check_and_log('equation',elem)

def enhance_equation_filter(doc:pf.Doc=None):
    return pf.run_filters(actions=[_enhance_equation],prepare=_prepare_enhance_equation,doc=doc)