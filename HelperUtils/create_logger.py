import logging
import logging.config
import yaml

with open('loggingConfig.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def create_logger(name):
    logger = logging.getLogger(name)
    logger.info(f'Setup logger!')
    return logger
