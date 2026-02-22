import logging
import logging.config
import os

from dotenv import load_dotenv
load_dotenv()

def configure_logger(logger_level=logging.INFO, log_path=None):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(asctime)s [%(levelname)s]: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': logger_level,
                'class': 'logging.StreamHandler',
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            'file': {
                'level': logger_level,
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'simple',
                'filename': log_path,
                'maxBytes': 1024,
                'backupCount': 3
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': logger_level,
                'propagate': True
            }
        }
    })