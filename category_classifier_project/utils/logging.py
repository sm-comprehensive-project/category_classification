# utils/logging.py
import logging
import sys
from pythonjsonlogger import jsonlogger  # pip install python-json-logger
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name="project", level="INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # 콘솔 출력 핸들러 (stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    # 🔽 파일 저장 핸들러 (회전형)
    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler("logs/project.log", maxBytes=1_000_000, backupCount=5)
    file_formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

log = setup_logger()
