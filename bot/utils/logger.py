import logging

LOG_LEVEL = logging.INFO

def setup_logger(name: str = "BOT") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    log_format = logging.Formatter(
        '[%(levelname)s]: %(asctime)s - %(message)s'
    )
    log_file = logging.FileHandler('logs/bot.log')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    log_file.setFormatter(log_format)
    logger.addHandler(log_file)
    return logger

logger = setup_logger()
