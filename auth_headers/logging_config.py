import logging


def configure_logging(logger_name: str = "root", level: str = "DEBUG") -> logging.Logger:
    """
    Configure logging to output only to terminal.
    
    :param logger_name: Logger name. Default is 'root'.
    :param level: Logging level.
    :return: Logger instance.
    """
    # Get the logger
    logger = logging.getLogger(logger_name)

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the logging level
    if level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif level == "INFO":
        logger.setLevel(logging.INFO)
    elif level == "WARNING":
        logger.setLevel(logging.WARNING)
    elif level == "ERROR":
        logger.setLevel(logging.ERROR)
    elif level == "CRITICAL":
        logger.setLevel(logging.CRITICAL)

    # Define a custom log format
    log_format = "%(asctime)s | %(filename)s | line:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s"

    # Create a StreamHandler to output logs to the terminal
    stream_handler = logging.StreamHandler()

    # Create a Formatter with the custom log format
    formatter = logging.Formatter(log_format)

    # Set the Formatter for the StreamHandler
    stream_handler.setFormatter(formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)

    return logger


# Create the main logger with WARNING level
main_logger = configure_logging(logger_name="main", level="WARNING")
