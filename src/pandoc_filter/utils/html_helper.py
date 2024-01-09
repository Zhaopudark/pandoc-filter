import re
import typeguard

def __get_attribute(text:str,attribute:str)->str|None:
    match = re.search(rf"{attribute}=['\"]([^'\"]+)['\"]",text)
    if match:
        return str(match.group(1))
    else:
        return None
def __sub_attribute(text:str,attribute:str,sub_string:str)->str:
    return re.sub(rf"({attribute}=['\"])([^'\"]+)(['\"])", f"\\g<1>{sub_string}\\g<3>", text)

# href
@typeguard.typechecked
def get_href(text:str)->str|None:
    return __get_attribute(text,"href")
    
@typeguard.typechecked
def sub_href(text:str,sub_string:str)->str:
    return __sub_attribute(text,"href",sub_string)

# id
@typeguard.typechecked
def get_id(text:str)->str|None:
    return __get_attribute(text,"id")
@typeguard.typechecked
def sub_id(text:str,sub_string:str)->str:
    return __sub_attribute(text,"id",sub_string)

# src
@typeguard.typechecked
def get_src(text:str)->str|None:
    return __get_attribute(text,"src")
@typeguard.typechecked
def sub_src(text:str,sub_string:str)->str:
    return __sub_attribute(text,"src",sub_string)