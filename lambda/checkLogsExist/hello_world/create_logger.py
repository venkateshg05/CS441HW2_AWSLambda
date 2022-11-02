import logging
import logging.config
import yaml


def create_logger(name):
    """
    creates the logger with the parameters defined in loggingConfig.yaml
    """
    with open('loggingConfig.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(name)
    logger.info(f'Setup logger!')
    return logger
