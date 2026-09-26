import logging

from config.config import PROJECT_ROOT


LOG_FILE = PROJECT_ROOT / "logs" / "pipeline.log"

LOG_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)


def get_logger() -> logging.Logger:
    """
    Configure and return the ETL pipeline logger.
    """
    logger = logging.getLogger("etl_pipeline")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger