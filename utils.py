#!/usr/bin/env python

from pathlib2 import Path
import os
import logging
import logging.handlers

"""
General utilities, particularly logging
"""


def initialize_logging(log_name=None, file_log_level=logging.DEBUG,
        console_log_level=logging.INFO,
        ci_log_name=os.environ.get('CI_LOG_NAME', 'common.log'),
        logging_directory=os.environ.get('WORKSPACE', '.'), verbose=False):
    """
    This implementation is in-between using the basic logging
    configuration and a fully custom system.
    """
    if not log_name:
        # Use the root logger. Since we don't have a nice module
        # structure, the __name__ trick doesn't help us and this has one
        # less layer that can get mis-configured. If you use the root
        # logger (opposed to a named logger) you don't need to keep the
        # returned logger, because "logging.info()" etc. will work. BTW,
        # logging.getLogger('') also returns the root.
        logger = logging.getLogger()
    else:
        # This is so you can give it a name (log_id) if you insist, and
        # it will be a child of the root. The log file will be named
        # after the log_id + '.log'
        logger = logging.getLogger(log_name)
        ci_log_name = "{}.log".format(log_name)
    if verbose:
        console_log_level = logging.DEBUG
    # Log name and path
    log_file = Path(logging_directory) / ci_log_name
    log_file.parent.mkdir(parents=True, exist_ok=True)
    # Set the overall lowest level to report
    logger.setLevel(logging.DEBUG)
    # Start with no handlers - This can be the cause of duplicate messages
    logger.handlers = []
    # File handler, logs everything
    fh = logging.handlers.RotatingFileHandler(str(log_file), mode='a',
        maxBytes=10 * 1024 * 1024, backupCount=5)
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
