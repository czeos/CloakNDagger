import logging.config
from pathlib import Path

from config import BASE_PATH
LOGS_DIR = BASE_PATH / Path('logs')

#check if logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

# logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO',
        },
        'file_info': {
            'class': 'logging.FileHandler',
            'filename': f'{LOGS_DIR}/info.log',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file_debug': {
            'class': 'logging.FileHandler',
            'filename': f'{LOGS_DIR}/debug.log',
            'formatter': 'detailed',
            'level': 'DEBUG'
        },
        'file_error': {
            'class': 'logging.FileHandler',
            'filename': f'{LOGS_DIR}/error.log',
            'formatter': 'detailed',
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file_info'],
            'level': 'INFO',
        },
        'app.module': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

