"""
pandoc-filter version
"""
from .utils import check_pandoc_version

check_pandoc_version(required_version='3.1.0')
__version__ = '0.1.0b1'