import logging
import sys
import structlog
from asgi_correlation_id import correlation_id

def configure_logger(is_production: bool = False):
    # 1. Inyectar el request_id mágico
    def add_correlation_id(logger, method_name, event_dict):
        req_id = correlation_id.get()
        if req_id:
            event_dict["request_id"] = req_id
        return event_dict

    # 2. Procesadores base compartidos (los usan tus Casos de Uso y Uvicorn)
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        add_correlation_id,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,  # ¡Ahora sí funcionará!
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # 3. Configurar Structlog para que mande todo al 'logging' nativo de Python
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(), # <--- LA SOLUCIÓN AL ERROR
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 4. Crear el embudo final (Consola bonita o JSON estricto)
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer() if is_production else structlog.dev.ConsoleRenderer()
        ],
    )

    # 5. Redirigir TODO Python hacia nuestro formateador Structlog
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.DEBUG)

    # 6. Silenciar el ruido por defecto de Uvicorn para que no haya logs duplicados
    for _log in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uvicorn_logger = logging.getLogger(_log)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True

    logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

def get_logger(name: str):
    return structlog.get_logger(name)