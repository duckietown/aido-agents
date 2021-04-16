__version__ = "6.0.19"

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
import os

path = os.path.dirname(os.path.dirname(__file__))
logger.debug(f"aido-agents version {__version__} path {path}")

from .utils_images import *
from .utils_leds import *
from .baseline_full_agent import *
