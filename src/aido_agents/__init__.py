__version__ = "6.0.6"

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
logger.info(f"aido-agents {__version__}")

from .utils_images import *
from .utils_leds import *
