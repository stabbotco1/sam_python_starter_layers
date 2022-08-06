"""
loguru_helper.py - contains functions and object to make logging with loguru easier 
"""
import sys
import time
import functools
import os
from loguru import logger
from logging import StreamHandler



valid_log_levels = ['TRACE' , 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
os_env_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = os_env_log_level if os_env_log_level in valid_log_levels else "INFO"

LOG_SEQUENCE_NUMBER = 0

def logger_wraps(*, entry=True, exit=True, level="INFO"):
    """
    Loguru decorator declaration

    Args:
        entry (bool, optional): _description_. Defaults to True.
            logs a function starting when set to true
        exit (bool, optional): _description_. Defaults to True.
            logs a functions exiting, with duration, when set to True
        level (str, optional): _description_. Defaults to "INFO".
            Log level logged when called
    """
    def wrapper(func):
        
        name = func.__name__
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            global LOG_SEQUENCE_NUMBER
            logger_ = logger.opt(depth=1)
            entry_time = 0.0        

            if entry:
                entry_time = time.time()
                LOG_SEQUENCE_NUMBER += 1
                logger_.log(level, f"Entering function:'{name}', \"log_sequence_number\"=\"{LOG_SEQUENCE_NUMBER}\", (\"args\"=\"{args}\", \"kwargs\"=\"{kwargs})\"")

            result = func(*args, **kwargs)
            if exit:
                function_duration = "{:.6f}".format(time.time() - entry_time)
                LOG_SEQUENCE_NUMBER += 1
                logger_.log(level, f"Exiting function:'{name}', \"log_sequence_number\"=\"{LOG_SEQUENCE_NUMBER}\", , \"duration\":\"{function_duration}\", (\"args\"=\"{args}\", \"kwargs\"=\"{kwargs})\"")
            return result
        return wrapped
    return wrapper

def logger_init():
    """
    Initializes the logger formatting output to be JSON and contain:
    - timestamp - iso8601 timestamp in UTC with 6 digits of accuracy
    - level - log level of the logged event
    - process - process ID running the code
    - thread - thread ID running the code
    - module - module running the code
    - file - file name running the code
    - line - line number when the log was emitted
    - message - log message passed in to the logging function
    """
    logger.remove(0)
    logger.add(StreamHandler(sys.stdout), format="{{\
\"timestamp\":\"{time:YYYY-MM-DD!UTC}T{time:HH:mm:ss.ssssss!UTC}-0000\"\
, \"level\":\"{level}\"\
, \"process\":\"{process}\"\
, \"thread\":\"{thread}\"\
, \"module\":\"{module}\"\
, \"file\":\"{file}\"\
, \"name\":\"{name}\"\
, \"line\":\"{line}\"\
, \"message\":\"{message}\"\
}}",\
        level=LOG_LEVEL)
    logger.debug("initialized logger")
    