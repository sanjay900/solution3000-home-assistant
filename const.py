"""Constants for the Detailed Hello World Push integration."""
from __future__ import annotations

from datetime import timedelta

import logging
from typing import Final

DOMAIN = "solutions3000"
SCAN_INTERVAL = timedelta(seconds=10)
LOGGER = logging.getLogger(__package__)

SERVICE_PANEL: Final = "panel"