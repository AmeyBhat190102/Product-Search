import sys
import time
import asyncio
import logging
import traceback
from functools import wraps
from loguru import logger  # type: ignore


# --- Singleton Metaclass for Logger Instance ---
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# --- Logging Level Mapping ---
LOG_LEVEL_MAPPING = {
    "CRITICAL": "CRITICAL",
    "ERROR": "ERROR",
    "WARNING": "WARNING",
    "INFO": "INFO",
    "DEBUG": "DEBUG",
    "NOTSET": "DEBUG",
}


# --- AppLogger Singleton (Using Loguru) ---
class AppLogger(metaclass=SingletonMeta):
    _logger = None

    def __init__(self):
        self._setup_logger()

    def _setup_logger(self):
        if self._logger is not None:
            return

        logger.remove()
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        class InterceptHandler(logging.Handler):
            def emit(self, record):
                try:
                    loguru_level = LOG_LEVEL_MAPPING.get(
                        record.levelname.upper(), "INFO"
                    )
                    message = record.getMessage()

                    if record.exc_info:
                        exception_info = "".join(
                            traceback.format_exception(*record.exc_info)
                        )
                        logger.opt(depth=6, exception=record.exc_info).log(
                            loguru_level, f"{message}\n{exception_info}"
                        )
                    else:
                        logger.opt(depth=6).log(loguru_level, message)
                except Exception as e:
                    logger.opt(depth=6).error(
                        f"Logging Interception Error: {e}\n{traceback.format_exc()}"
                    )

        intercept_handler = InterceptHandler()

        logging.root.handlers.clear()
        logging.root.addHandler(intercept_handler)
        logging.root.setLevel(logging.INFO)

        for logger_name in logging.root.manager.loggerDict.keys():
            log = logging.getLogger(logger_name)
            log.handlers.clear()
            log.addHandler(intercept_handler)
            log.setLevel(logging.INFO)
            log.propagate = False

        self._logger = logger

    @classmethod
    def get_logger(cls):
        instance = cls()
        return instance._logger


# --- Global Loguru Logger ---
app_logger = AppLogger.get_logger()


# --- Decorator to Log Execution Time ---
def log_execution_time(func):
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            app_logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result

        return async_wrapper

    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            app_logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result

        return sync_wrapper
