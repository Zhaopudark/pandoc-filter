"""
See https://github.com/Zhaopudark/pandoc-filter for documentation.
"""
import logging

from . import filters

# from .filters.md2md.convert_github_style_alert_to_hexo_style_alert \
#     import run_filter as md2md_convert_github_style_alert_to_hexo_style_alert_filter
# from .filters.md2md.enhance_equation import run_filter as md2md_enhance_equation_filter
# from .filters.md2md.norm_footnote import run_filter as md2md_norm_footnote_filter
# from .filters.md2md.norm_internal_link import run_filter as md2md_norm_internal_link_filter
# from .filters.md2md.upload_figure_to_aliyun import run_filter as md2md_upload_figure_to_aliyun_filter
# from .filters.md2html.centralize_figure import run_filter as md2html_centralize_figure_filter
# from .filters.md2html.enhance_footnote import run_filter as md2html_enhance_footnote_filter
# from .filters.md2html.enhance_link_like import run_filter as md2html_enhance_link_like_filter
# from .filters.md2html.hash_anchor_and_internal_link import run_filter as md2html_hash_anchor_and_internal_link_filter
# from .filters.md2html.increase_header_level import run_filter as md2html_increase_header_level_filter

from .scripts import run_filters_pyio

from .version import __version__

from .utils.logging_helper import TracingLogger

logger = TracingLogger("./logs/pandoc_filter_log",level=logging.DEBUG)