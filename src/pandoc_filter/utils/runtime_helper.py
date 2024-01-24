from typing import Any
import typeguard
from collections import UserDict

class RuntimeStatusDict(UserDict):
    @typeguard.typechecked
    def lazy_update(self,key:str,value:Any)->None:
        if key not in self:
            self[key] = value
        elif self[key] != value:
            self[key] = value
        else:
            return None