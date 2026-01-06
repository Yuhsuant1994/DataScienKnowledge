from app.log.structlog import api_error_logger as structlog_api_error_logger
from app.log.structlog import api_logger as structlog_api_logger
from app.log.structlog import configure_logging as structlog_configure_logging
from app.log.structlog import default_logger as structlog_default_logger

default_logger = structlog_default_logger
api_logger = structlog_api_logger
api_error_logger = structlog_api_error_logger
configure_logging = structlog_configure_logging
