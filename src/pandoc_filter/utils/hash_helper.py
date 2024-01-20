import hashlib
import urllib.parse

def get_hash(text:str)->str:
    """
    Normalize the input text to a hash string. This is the global hash function for this project.
    
    There are several steps to normalize the input text:
        1. Decode the url-encoded text.
        2. Strip the leading and trailing spaces.
        3. Lower the text.
        4. Hash the text.
    """
    text = urllib.parse.unquote(text).strip(' ').lower() # 需要统一小写以获取更大的兼容性
    return hashlib.sha256(text.encode('utf-8')).hexdigest()