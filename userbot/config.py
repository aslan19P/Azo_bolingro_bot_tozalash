"""Configuration helpers for the Telegram userbot cleaner."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Tuple

try:  # pragma: no cover - optional dependency
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


@dataclass(frozen=True, slots=True)
class UserBotSettings:
    """Holds configuration required for the Telethon-based userbot."""

    api_id: int
    api_hash: str
    session_name: str
    phone_number: str | None
    target_chat_ids: Tuple[int, ...]
    target_chat_usernames: Tuple[str, ...]
    monitored_user_ids: Tuple[int, ...]
    monitored_user_usernames: Tuple[str, ...]
    match_keywords: Tuple[str, ...]
    delete_delay_seconds: int
    log_level: str

    DEFAULT_SESSION_NAME: str = "userbot_session"
    DEFAULT_DELETE_DELAY_SECONDS: int = 120
    DEFAULT_LOG_LEVEL: str = "INFO"

    @classmethod
    def from_env(cls) -> "UserBotSettings":
        if load_dotenv is not None:
            load_dotenv()

        def _require(name: str) -> str:
            value = os.getenv(name)
            if not value:
                raise RuntimeError(f"Environment variable {name} must be set for the userbot")
            return value

        def _parse_csv(value: str | None) -> Tuple[str, ...]:
            if not value:
                return ()
            return tuple(
                item.strip()
                for item in value.split(",")
                if item.strip()
            )

        def _parse_int_csv(value: str | None) -> Tuple[int, ...]:
            parsed: list[int] = []
            if not value:
                return ()
            for item in value.split(","):
                item = item.strip()
                if not item:
                    continue
                try:
                    parsed.append(int(item))
                except ValueError as exc:  # pragma: no cover - guard configuration
                    raise RuntimeError(f"Failed to parse integer from '{item}'") from exc
            return tuple(parsed)

        api_id_raw = _require("USERBOT_API_ID")
        try:
            api_id = int(api_id_raw)
        except ValueError as exc:  # pragma: no cover - guard configuration
            raise RuntimeError("USERBOT_API_ID must be an integer") from exc

        api_hash = _require("USERBOT_API_HASH")
        session_name = os.getenv("USERBOT_SESSION_NAME", cls.DEFAULT_SESSION_NAME)
        phone_number = os.getenv("USERBOT_PHONE_NUMBER")

        target_chat_ids = _parse_int_csv(os.getenv("USERBOT_TARGET_CHAT_IDS"))
        target_chat_usernames = tuple(
            name.lower().lstrip("@")
            for name in _parse_csv(os.getenv("USERBOT_TARGET_CHAT_USERNAMES"))
        )
        monitored_user_ids = _parse_int_csv(os.getenv("USERBOT_MONITORED_USER_IDS"))
        monitored_user_usernames = tuple(
            name.lower().lstrip("@")
            for name in _parse_csv(os.getenv("USERBOT_MONITORED_USERNAMES"))
        )
        match_keywords = _parse_csv(os.getenv("USERBOT_MATCH_KEYWORDS"))

        delay_raw = os.getenv("USERBOT_DELETE_DELAY_SECONDS")
        try:
            delete_delay = (
                int(delay_raw) if delay_raw else cls.DEFAULT_DELETE_DELAY_SECONDS
            )
        except ValueError as exc:  # pragma: no cover - guard configuration
            raise RuntimeError("USERBOT_DELETE_DELAY_SECONDS must be an integer") from exc

        log_level_raw = os.getenv("USERBOT_LOG_LEVEL", cls.DEFAULT_LOG_LEVEL)
        log_level = log_level_raw.upper()
        if log_level not in logging._nameToLevel:  # pragma: no cover - guard configuration
            raise RuntimeError(
                "Unknown USERBOT_LOG_LEVEL '"
                + log_level_raw
                + "'. Expected one of: "
                + ", ".join(sorted(logging._nameToLevel))
            )

        if not target_chat_ids and not target_chat_usernames:
            raise RuntimeError(
                "Provide at least one of USERBOT_TARGET_CHAT_IDS or USERBOT_TARGET_CHAT_USERNAMES"
            )

        if not monitored_user_ids and not monitored_user_usernames and not match_keywords:
            raise RuntimeError(
                "Configure USERBOT_MONITORED_USER_IDS, USERBOT_MONITORED_USERNAMES or USERBOT_MATCH_KEYWORDS"
            )

        return cls(
            api_id=api_id,
            api_hash=api_hash,
            session_name=session_name,
            phone_number=phone_number,
            target_chat_ids=target_chat_ids,
            target_chat_usernames=target_chat_usernames,
            monitored_user_ids=monitored_user_ids,
            monitored_user_usernames=monitored_user_usernames,
            match_keywords=match_keywords,
            delete_delay_seconds=delete_delay,
            log_level=log_level,
        )

    def describe_targets(self) -> str:
        pieces: list[str] = []
        if self.target_chat_ids:
            pieces.append("ids=" + ",".join(str(_id) for _id in self.target_chat_ids))
        if self.target_chat_usernames:
            pieces.append("usernames=" + ",".join(self.target_chat_usernames))
        return "; ".join(pieces)

    def describe_filters(self) -> str:
        pieces: list[str] = []
        if self.monitored_user_ids:
            pieces.append("user_ids=" + ",".join(str(_id) for _id in self.monitored_user_ids))
        if self.monitored_user_usernames:
            pieces.append("usernames=" + ",".join(self.monitored_user_usernames))
        if self.match_keywords:
            pieces.append("keywords=" + ",".join(self.match_keywords))
        return "; ".join(pieces)


SettingsLike = UserBotSettings
