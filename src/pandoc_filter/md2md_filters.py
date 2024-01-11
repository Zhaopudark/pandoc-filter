import logging
import re
import typeguard
import urllib.parse
import pathlib
import panflute as pf
from .utils.logging_helper import TracingLogger
from .utils.oss_helper import OssHelper
from .utils import html_helper
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
    elif isinstance(elem, pf.RawInline) and elem.format == 'html' and (old_href:=html_helper.get_href(elem.text)) and old_href.startswith('#'):
        tracing_logger.mark(elem)
        elem.text = html_helper.sub_href(elem.text,_decode_internal_link_url(old_href))
        tracing_logger.check_and_log('raw_anchor_links',elem)


@typeguard.typechecked
def math_filter(elem:pf.Element,doc:pf.Doc,**kwargs)->None: # Modify In Place
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to process math formula when converting markdown to markdown.
    To realize:
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
    if not(hasattr(doc,'have_math') and isinstance(doc.have_math,bool)):
        doc.have_math = False
    if isinstance(elem, pf.elements.Math):
        if not doc.have_math: # lazy modification
            doc.have_math = True
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

@typeguard.typechecked     
def figure_filter(elem:pf.Element,doc:pf.Doc,**kwargs)->None: # Modify In Place
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to process images of local pictures when converting markdown to markdown.
    Manager local pictures, sync them to Aliyun OSS, and replace the original src with the new one.
    NOTE
        The `doc.doc_path` should be set before calling this filter.
        The `doc.doc_path` should be a pathlib.Path object.
        The local pictures should be within the same directory as the doc file.
    """
    oss_helper:OssHelper = kwargs['oss_helper']
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if not(hasattr(doc,'doc_path') and isinstance(doc.doc_path,pathlib.Path)):
        tracing_logger.logger.warning("doc.doc_path is not set or is not a pathlib.Path object.")
        return None    
    if isinstance(elem, pf.Image) and (old_src:=str(elem.url)).startswith('.'): # reletive path
        new_src = oss_helper.maybe_upload_file_and_get_src(doc.doc_path.parent/old_src)
        tracing_logger.mark(elem)
        elem.url = new_src
        tracing_logger.check_and_log('image',elem)
    elif isinstance(elem, pf.RawInline) and elem.format == 'html' and (old_src:=html_helper.get_src(elem.text)) and old_src.startswith('.'): # reletive path
            new_src = oss_helper.maybe_upload_file_and_get_src(doc.doc_path.parent/old_src)
            tracing_logger.mark(elem)
            elem.text = html_helper.sub_src(elem.text,new_src)
            tracing_logger.check_and_log('raw_html_img',elem)

@typeguard.typechecked
def footnote_filter(elem:pf.Element,doc:pf.Doc,**kwargs)->pf.Note|None: # Repleace
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    A filter to process footnotes. Remove `\n` in the footnote content.
    """
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if isinstance(elem, pf.Note):
        tracing_logger.mark(elem)
        elem = pf.Note(pf.Para(pf.Str(pf.stringify(elem.content).strip(" \n"))))
        tracing_logger.check_and_log('footnote',elem)
        return elem

