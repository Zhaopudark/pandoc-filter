from typing import Any,TypedDict
import typeguard
import pathlib
from collections import UserDict
import panflute as pf

from .logging_helper import TracingLogger
from .html_helper import sub_html_href
from .oss_helper import OssHelper
        
class InternalLink():
    @typeguard.typechecked
    def __init__(self,elem:pf.Link|pf.RawInline,url:str,guessed_url:str|None) -> None:
        self.elem = elem
        self.url = url
        self.guessed_url = guessed_url
    @typeguard.typechecked
    def sub(self,text:str,tracing_logger:TracingLogger)->None:
        tracing_logger.mark(self.elem)
        if isinstance(self.elem, pf.Link):
            self.elem.url = f"#{text}"
        else: # RawInline
            self.elem.text = sub_html_href(self.elem.text,f"#{text}")
        tracing_logger.check_and_log('internal_link',self.elem)

class DocRuntimeDict(TypedDict):
    anchor_count:dict[str,int]|None
    internal_link_record:list[InternalLink]|None
    equations_count:int|None
    math:bool|None
    doc_path:pathlib.Path|None
    oss_helper:OssHelper|None