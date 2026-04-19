import logging
import os
from logging.handlers import TimedRotatingFileHandler
import colorlog
from typing import Optional, List

class ExcludeErrorsFilter(logging.Filter):
    def __init__(self, excluded_phrases: List[str]):
        super().__init__()
        self.excluded_phrases = excluded_phrases
    
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(phrase in message for phrase in self.excluded_phrases)

class BotLogger:
    _initialized = False
    EXCLUDED_PHRASES = [
        "message is not modified",
        "ServerDisconnectedError",
        "Sleep for 1.000000 seconds and try again"
    ]
    
    @classmethod
    def setup(cls, log_level: str = "INFO", excluded_phrases: Optional[List[str]] = None):
        if cls._initialized:
            return
            
        LOG_DIR = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'logs'
        )
        os.makedirs(LOG_DIR, exist_ok=True)
        
        log_file = os.path.join(LOG_DIR, 'bot.log')
        
        file_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'white',
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        file_handler = TimedRotatingFileHandler(
            log_file,
            when="W0",
            backupCount=4,
            encoding='utf-8',
            utc=True
        )
        file_handler.setFormatter(file_formatter)
        file_handler.suffix = "%Y-%W"
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        
        all_excluded = cls.EXCLUDED_PHRASES + (excluded_phrases or [])
        error_filter = ExcludeErrorsFilter(all_excluded)
        file_handler.addFilter(error_filter)
        console_handler.addFilter(error_filter)
        
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, log_level))
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        cls._initialized = True
        logger.debug("Логирование инициализировано. Папка для логов: %s", LOG_DIR)

        aiogram_logger = logging.getLogger("aiogram")
        aiogram_logger.setLevel(logging.WARNING)

def get_logger(name: Optional[str] = None) -> logging.Logger:
    if not BotLogger._initialized:
        BotLogger.setup()
    return logging.getLogger(name or "root")