import asyncio
from app.infraestructure.logger import configure_logger, get_logger

configure_logger()
logger = get_logger("test")

logger.info("this is an info", amount=1)
logger.warning("this is a warning", amount=-1)
logger.error("this is an error")
