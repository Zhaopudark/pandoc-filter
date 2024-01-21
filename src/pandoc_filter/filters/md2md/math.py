import re
import typeguard
import panflute as pf

from ...utils import TracingLogger

@typeguard.typechecked
def math_filter(elem:pf.Element,doc:pf.Doc,**kwargs)->None: # Modify In Place
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to process math formula when converting markdown to markdown.
    
    To realize:
        - Add `math: true` to metadata when there is math formula.
        - Adapt AMS rule for math formula
            - Auto numbering markdown formulations within \begin{equation} \end{equation}, as in Typora
        - Allow multiple tags, but only take the first one.
        - Allow multiple labels, but only take the first one.
        
    To make equations recognized correctly, content like the following irregular syntax should to be avoided:
    
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
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if not(hasattr(doc,'equations_count') and isinstance(doc.equations_count,int) and (doc.equations_count >= 0)):
        doc.equations_count = 0
    if isinstance(elem, pf.elements.Math):
        doc.metadata['math'] = True
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
                    doc.equations_count += 1
                    text = f"\\begin{{equation}}{first_label}\\tag{{{doc.equations_count}}}\n{text.strip(" \n")}\n\\end{{equation}}"
            else:
                text = f"{text}\n{first_label}{first_tag}"
            elem.text = f"\n{text.strip(" \n")}\n"
            tracing_logger.check_and_log('equation',elem)