import logging

# Logger configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s: %(message)s"
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
