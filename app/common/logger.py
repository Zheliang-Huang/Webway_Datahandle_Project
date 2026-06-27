import os

import logging.handlers
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent


def init_logger(log_name, log_dir, log_level=logging.INFO):
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    log_path = log_dir / f'{log_name}_{datetime.now().strftime("%Y%m%d")}.log'

    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")

    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger = logging.getLogger()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
