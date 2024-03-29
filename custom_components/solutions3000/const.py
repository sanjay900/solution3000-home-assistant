from __future__ import annotations

from datetime import timedelta

import logging
from typing import Final

DOMAIN = "solutions3000"
SCAN_INTERVAL = timedelta(seconds=1)

SERVICE_PANEL: Final = "panel"
CONF_HISTORY = "show_history"
CONF_REQUIRE_PIN = "require_pin"
CONF_HISTORY_COUNT = "history_count"