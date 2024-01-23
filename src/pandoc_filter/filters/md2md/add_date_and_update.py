import pathlib
import datetime
import functools

import typeguard
import panflute as pf


from ...utils import TracingLogger

r"""A pandoc filter that mainly for converting `markdown` to `markdown`.
Add date and update time to metadata.
NOTE:
    The doc_path should be given in advance.
"""
@typeguard.typechecked
def _prepare_add_date_and_update(doc:pf.Doc,*,doc_path:pathlib.Path)->None:
    doc.metadata['date'] = datetime.datetime.fromtimestamp(doc_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    doc.metadata['updated'] = datetime.datetime.fromtimestamp(doc_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')

@typeguard.typechecked
def add_date_and_update_filter(doc:pf.Doc=None,doc_path:pathlib.Path=None):
    __prepare_add_date_and_update = functools.partial(_prepare_add_date_and_update,doc_path=doc_path)
    return pf.run_filters(actions=[],prepare=__prepare_add_date_and_update,doc=doc)