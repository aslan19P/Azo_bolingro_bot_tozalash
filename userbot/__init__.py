"""Public API for the Telethon-based userbot cleaner."""

from .cleaner import main
from .config import UserBotSettings

__all__ = ["main", "UserBotSettings"]
