import logging
from logging import Formatter, Logger, StreamHandler


class CustomFormatter(Formatter):
    grey: str = "\x1b[38;20m"
    yellow: str = "\x1b[37;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"
    format: str = "%(asctime)s %(levelname)s - %(message)s"

    FORMATS: dict = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record) -> str:
        log_fmt: str = self.FORMATS.get(record.levelno)
        formatter: Formatter = Formatter(fmt=log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def load_custom_logger() -> Logger:
    log: Logger = logging.getLogger()
    log.setLevel(logging.INFO)

    sh: StreamHandler = StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(CustomFormatter())

    log.addHandler(sh)

    return log
