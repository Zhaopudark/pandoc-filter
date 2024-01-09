#!/usr/bin/env python
import logging
import functools
import logging
import typeguard
import panflute as pf
from pandoc_filters.utils.logging_helper import TracingLogger,logger_factory
from pandoc_filters.pandoc_checker import check_pandoc_version
from pandoc_filters.md2html_filters import anchor_filter,internal_link_recorder,link_like_filter


@typeguard.typechecked
def finalize(doc:pf.Doc,**kwargs):
    tracing_logger = kwargs['tracing_logger']
    logger = kwargs['logger']
    id_set = set()
    for k,v in doc.anchor_count.items():
        for i in range(1,v+1):
            id_set.add(f"{k}-{i}")
    for patched_elem,url,guessed_url_with_num in doc.internal_link_record:
        if f"{url}-1" in id_set:
            patched_elem.sub(f"{url}-1",tracing_logger)
        elif guessed_url_with_num in id_set: # None is not in id_set
            patched_elem.sub(f"{guessed_url_with_num}",tracing_logger)
        else:
            logger.warning(f"{patched_elem.elem}")
            logger.warning(f"The internal link `{url}` is invalid and will not be changed because no target header is found.")
       
    
def main(doc=None,**kwargs):
    check_pandoc_version(required_version='3.1.0')
    _finalize = functools.partial(finalize,**kwargs)
    return pf.run_filters(actions= [anchor_filter,internal_link_recorder,link_like_filter],finalize=_finalize,doc=doc,**kwargs)

if __name__ == "__main__":
    tracing_logger = TracingLogger(name='logs/pf_log',level=logging.WARNING)
    logger = logger_factory(name='logs/pf_log',level=logging.WARNING)
    main(tracing_logger=tracing_logger,logger=logger)