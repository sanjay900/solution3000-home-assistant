from __future__ import annotations

from datetime import timedelta

import logging
from typing import Final

DOMAIN = "solution3000"
SCAN_INTERVAL = timedelta(seconds=1)
LOGGER = logging.getLogger(__package__)

SERVICE_PANEL: Final = "panel"
