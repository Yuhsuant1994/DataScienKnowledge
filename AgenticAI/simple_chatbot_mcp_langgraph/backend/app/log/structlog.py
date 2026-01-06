import logging
import sys

import structlog


def set_level(logger_name: str, level_name: str):
    logging.getLogger(logger_name).setLevel(
        logging._nameToLevel.get(level_name.upper(), 0)
    )


def configure_logging(enable_json_logs: bool = False):
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M:%SZ")

    shared_processors = [
        timestamper,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.contextvars.merge_contextvars,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.THREAD,
                structlog.processors.CallsiteParameter.THREAD_NAME,
                structlog.processors.CallsiteParameter.PROCESS,
                structlog.processors.CallsiteParameter.PROCESS_NAME,
            }
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info if enable_json_logs else None,
        structlog.stdlib.ExtraAdder(),
    ]

    shared_processors = list(filter(lambda x: x is not None, shared_processors))
    structlog.configure(
        processors=shared_processors
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logs_render = (
        structlog.processors.JSONRenderer(ensure_ascii=False)
        if enable_json_logs
        else structlog.dev.ConsoleRenderer(
            colors=True,
            exception_formatter=structlog.dev.better_traceback,
        )
    )

    _configure_default_logging_by_custom(shared_processors, logs_render)


def _configure_default_logging_by_custom(shared_processors, logs_render):
    handler = logging.StreamHandler()

    # Use `ProcessorFormatter` to format all `logging` entries.
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            _extract_from_record,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            logs_render,
        ],
    )

    handler.setFormatter(formatter)
    root_uvicorn_logger = logging.getLogger()
    root_uvicorn_logger.addHandler(handler)
    root_uvicorn_logger.setLevel(logging.INFO)

    es_logger = logging.getLogger("elastic_transport.transport")
    es_logger.setLevel(logging.ERROR)

    for _log in ["uvicorn", "uvicorn.error"]:
        # Clear the log handlers for uvicorn loggers, and enable propagation
        # so the messages are caught by our root logger and formatted correctly
        # by structlog
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True

    # rename logger name uvicorn.error to uvicorn.server to avoid misunderstanding
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.name = "uvicorn.server"

    # Since we re-create the access logs ourselves, to add all information
    # in the structured log (see the `logging_middleware` in main.py), we clear
    # the handlers and prevent the logs to propagate to a logger higher up in the
    # hierarchy (effectively rendering them silent).
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = False

    def handle_exception(exc_type, exc_value, exc_traceback):
        """
        Log any uncaught exception instead of letting it be printed by Python
        (but leave KeyboardInterrupt untouched to allow users to Ctrl+C to stop)
        See https://stackoverflow.com/a/16993115/3641865
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_uvicorn_logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception


def _extract_from_record(_, __, event_dict):
    # Extract thread and process names and add them to the event dict.
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName
    event_dict["severity"] = record.levelname

    return event_dict


default_logger = structlog.stdlib.get_logger("default")
api_logger = structlog.stdlib.get_logger("api.access")
api_error_logger = structlog.stdlib.get_logger("api.error")

set_level("default", "DEBUG")
set_level("api.access", "INFO")
