"""
See https://github.com/Zhaopudark/pandoc-filter for documentation.
"""
import logging

from .filters.md2md import enhance_equation_filter as md2md_enhance_equation_filter
from .filters.md2md import norm_footnote_filter as md2md_norm_footnote_filter
from .filters.md2md import norm_internal_link_filter as md2md_norm_internal_link_filter
from .filters.md2md import upload_figure_to_aliyun_filter as md2md_upload_figure_to_aliyun_filter
from .filters.md2html import centralize_figure_filter as md2html_centralize_figure_filter
from .filters.md2html import enhance_link_like_filter as md2html_enhance_link_like_filter
from .filters.md2html import hash_anchor_and_internal_link_filter as md2html_hash_anchor_and_internal_link_filter

from .scripts import run_filters_pyio

from .version import __version__

from .utils import TracingLogger

logger = TracingLogger("./logs/pandoc_filter_log",level=logging.DEBUG)