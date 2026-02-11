# ##############
# ### LOGGER ###
# ##############


# ### Imports ###

from boxes_tui.shared_vars import SHARED_VARS
from enum import Enum
import os


# ### Helper functions ###

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

def set_log_file(path: str, clear_log_file: bool = True) -> bool:
    if not os.path.exists(path):
        open(path, 'w').close()

    SHARED_VARS["LOG_FILE"] = path
    if clear_log_file:
        open(SHARED_VARS["LOG_FILE"], 'w').close()
    log(LogLevel.INFO, f'Set logfile to "{SHARED_VARS["LOG_FILE"]}"')
    return True

def set_log_level(new_level) -> None:
    if isinstance(new_level, int):
        SHARED_VARS["LOG_LEVEL"] = new_level
    elif isinstance(new_level, LogLevel):
        SHARED_VARS["LOG_LEVEL"] = new_level.value


# ### Main function ###

def log(log_level: int, message: str) -> bool:
    if SHARED_VARS["LOG_FILE"] is None:
        return False
    if SHARED_VARS["LOG_LEVEL"] > log_level.value:
        return True

    log_level_prefix = ''
    if log_level == LogLevel.DEBUG:
        log_level_prefix = "DEBUG: "
    elif log_level == LogLevel.INFO:
        log_level_prefix = "INFO: "
    elif log_level == LogLevel.WARNING:
        log_level_prefix = "WARNING: "
    elif log_level == LogLevel.ERROR:
        log_level_prefix = "ERROR: "
    elif log_level == LogLevel.CRITICAL:
        log_level_prefix = "CRITICAL: "

    with open(SHARED_VARS["LOG_FILE"], 'a') as log_file:
        log_file.write(log_level_prefix + message + '\n')
    
    return True