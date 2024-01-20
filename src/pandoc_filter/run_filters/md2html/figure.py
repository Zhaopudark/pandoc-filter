import typeguard
import logging
import panflute as pf

from ...utils import TracingLogger
from ...utils import check_pandoc_version

@typeguard.typechecked     
def _figure_filter_v1(elem:pf.Element,doc:pf.Doc,**kwargs)->None: # Modify In Place:
    r"""Follow the general procedure of [Panflute](http://scorreia.com/software/panflute/)
    Deprecated. 
    The best way is to use CSS files to define global styles and use them by `--css <css_files>`,
    instead of make a filter here.
    So, this method is deprecated.        
    
    When converting markdown to html, Pandoc will generate a `Figure` element for each image,
    and copy the `alt_text` in `![image_url](alt_text)` to the `Caption` part of the `Figure`.
    
    And if in many Blog systems, the `alt_text` in `Image` will be copied again into the `Figure`,
    parallel with the original `Caption` part. Leading to dual captions in html.
    
    A not-so-good solution is to delete/elimiate the `Caption` part of the `Figure` element,
    which relys on the post-processing of the html file.
    
    A better way is to set inline styles on the `Figure` element, which does not rely on
    the post-processing components.
    
    Since in `Panflute`, the `Caption` element has no attributes, it is hard to modify it.
    So, we have to insert a `Div` element into the `Caption` element, and modify the `Div`
    element to show our target `alt_text`.
    
    And, it is better if set a global style `text-align:center` for the whole `Figure` element,
    which will not only influence the `Caption` part, but also the `Image` part.
    
    Even though in some Blog systems, the `Figure` element will be centered automatically,
    it is still a good practice to set the style in the `Figure` element, which will not
    be limited by post-processing components.
    
    For specific, the `Figure` element will be modified as:
        - add `text-align:center;` to the `style` attribute of the `Figure` element
        - new a `Caption` element, which includes a new `Div` element that contains the original `alt_text`
        - add `color:#858585;` to the `style` attribute of the `Div` element
        - replace the original `Caption` element with the new one.
    """
    logging.warning("""
    The figure filter is deprecated. Please use CSS files to define global styles and use them by `--css <css_files>`.
    See https://github.com/Zhaopudark/pandoc-filter/blob/main/src/pandoc_filter/run_filters/md2html/figure.py#L9 for more details.
    """)
    tracing_logger:TracingLogger = kwargs['tracing_logger']
    if isinstance(elem, pf.Figure):
        tracing_logger.mark(elem)
        for img in elem.content:
            if isinstance(img, pf.Image):
                break
        if 'style' in elem.attributes:
            elem.attributes['style'] += "text-align:center;"
        else:
            elem.attributes = {'style':"text-align:center;"}
        centered_div = pf.Div(*elem.caption.content,attributes={'style':"color:#858585;"})
        elem.caption = pf.Caption(centered_div)
        tracing_logger.check_and_log('figure',elem)

def main(doc=None,**kwargs):
    check_pandoc_version(required_version='3.1.0')
    tracing_logger = TracingLogger(name='logs/pf_log',level=logging.WARNING)
    return pf.run_filters(
        actions= [_figure_filter_v1],
        doc=doc,
        tracing_logger=tracing_logger,
        **kwargs)