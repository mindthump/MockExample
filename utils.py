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

    IMPORTANT:
    For each Python session, this function should be called first and only once.
    """
    if not log_name:
        # By default use the root logger. Since we don't have a nice
        # module structure, the __name__ trick doesn't help us and this
        # has one less layer that can get mis-configured. If you use the
        # root logger (opposed to a named logger) you don't need to keep
        # a reference to the returned logger, because "logging.info()"
        # etc. will just work. BTW, logging.getLogger('') and
        # logging.root also return the root logger.
        logger = logging.getLogger()
    else:
        # This is so you can give it a name if you insist, and it will
        # be created as a child of the root. The log file will be named
        # <log_name> + '.log'
        logger = logging.getLogger(log_name)
        ci_log_name = "{}.log".format(log_name)
    if verbose:
        # verbose option: Show debug messages on the console as well.
        console_log_level = logging.DEBUG
    # Log name and path using pathlib2
    log_file_path = Path(logging_directory) / ci_log_name
    # Path.resolve() obsoletes all the manual path munging (abspath, etc.).
    log_file_path.resolve()
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    # Set the overall lowest level to report
    logger.setLevel(logging.DEBUG)

    # Handlers
    # A logging object (e.g., the "logging" root or a named logger)
    # by itself does not output anything; it collects, holds, and
    # distributes the log records to its "handlers". All output is done
    # through its handlers, and any logging object can have multiple
    # handlers. The most common handlers are for files, and streams like
    # the console. When and where each handler outputs the records can
    # be customized.
    # Start with no handlers - This can be the cause of duplicate messages
    logger.handlers = []

    # Create a File handler and customize it
    # RotatingFileHandler: when the current log gets full it
    # automatically rotates the current file to a numbered backup and
    # creates a new empty log.
    file_handler = logging.handlers.RotatingFileHandler(str(log_file_path), mode='a',
        maxBytes=10 * 1024 * 1024, backupCount=5)
    # Log level (for this handler only)
    file_handler.setLevel(file_log_level)
    # Formatter to specify the "look" of the output lines (for this handler only)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(module)s.%(funcName)s() - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    # Add the customized handler to the logging object
    logger.addHandler(file_handler)

    # Create a Console handler and customize it
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Save some values so they're easy to get to. First, a Path object...
    # NOTE: str(logging.log_file_path.parent)
    # is the best practice to get the absolute logging directory.
    logging.log_file_path = log_file_path
    # If necessary, the absolute path to the file as a string is here.
    logging.log_file = str(log_file_path)
    # Return the new logger instance -- only useful for a named logger,
    # otherwise "import logging" will always work.
    return logger
