#!/usr/bin/env python

from pathlib2 import Path
import os
import logging
import logging.handlers

"""
General utilities, particularly logging
"""


def initialize_logging(file_log_level=logging.DEBUG, console_log_level=logging.INFO,
        ci_log_name=os.environ.get('CI_LOG_NAME', 'common.log'),
        fw_root=os.environ.get('WORKSPACE', '.')):

    # Log name and path
    log_file = Path(fw_root) / ci_log_name
    log_file.parent.mkdir(parents=True, exist_ok=True)
    # The root logger. Since we don't have a nice module structure, the
    # __name__ trick doesn't help us.
    logger = logging.getLogger()
    # Set the overall lowest level to report
    logger.setLevel(logging.DEBUG)
    # Start with no handlers - This can be the cause of duplicate messages
    logger.handlers = []
    # File handler which logs everything
    fh = logging.handlers.RotatingFileHandler(str(log_file), mode='a',
        maxBytes=1024 * 1024, backupCount=5)
    fh.setLevel(file_log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(module)s.%(funcName)s() - %(levelname)s - %(message)s')
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)
    # Console handler, generally only for INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(console_log_level)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

    return logger
