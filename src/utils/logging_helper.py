import typeguard
import logging
import logging.handlers
from typing import Any
@typeguard.typechecked
def logger_factory(name:str,level:int=logging.INFO)->logging.Logger:
    r"""Generate a logger with file and console handler.
    Args:
        name: the name of the logger and the indicator of the log file
        level: the level of the logger
    Returns:
        logger: an instance of logging.Logger that has been configured
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # check if the console handler exists
    console_handler_exists = any(
        isinstance(handler, logging.StreamHandler)
        for handler in logger.handlers
    )
    file_handler_exists = any(
        isinstance(handler, logging.FileHandler)
        for handler in logger.handlers
    )    
    file_handler = logging.handlers.RotatingFileHandler(
        f"{name}.log",
        maxBytes=2*1024*1024,
        backupCount=5,encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    if not file_handler_exists:
        logger.addHandler(file_handler)
    if not console_handler_exists:
        logger.addHandler(console_handler)
    logger.propagate = False
    return logger

class TracingLogger:
    def __init__(self,name:str,level:int=logging.INFO) -> None:
        self.logger = logger_factory(name=name,level=level)
        self.__buf = None
    def mark(self,buf:Any):
        self.__buf = str(buf)
    def check_and_log(self,indicator:str,buf:Any):
        if self.__buf != str(buf):
            self.logger.info(f"---{indicator}:{self.__buf}")
            self.logger.info(f"+++{indicator}:{str(buf)}")