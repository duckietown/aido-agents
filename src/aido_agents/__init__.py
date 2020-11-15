__version__ = "6.0.13"

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
logger.debug(f"aido-agents version {__version__} path {__file__}")

from .utils_images import *
from .utils_leds import *
from .baseline_full_agent import *
