"""Telethon-based userbot that removes unwanted messages from a group."""

from __future__ import annotations

import asyncio
import logging
from typing import Iterable

from telethon import TelegramClient, events
from telethon.errors import RPCError

from .config import UserBotSettings

logger = logging.getLogger(__name__)


def _normalize(username: str | None) -> str:
    return username.lower().lstrip("@") if username else ""


def _matches_any(text: str | None, keywords: Iterable[str]) -> bool:
    if not keywords:
        return True
    if not text:
        return False
    lowered = text.casefold()
    return any(keyword.casefold() in lowered for keyword in keywords)


async def _delete_later(
    client: TelegramClient, chat_id: int, message_id: int, delay: int
) -> None:
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_id)
        logger.info(
            "Deleted message chat_id=%s message_id=%s", chat_id, message_id
        )
    except RPCError as exc:
        logger.warning(
            "Failed to delete message chat_id=%s message_id=%s error=%s",
            chat_id,
            message_id,
            exc,
        )


async def _handle_event(
    event: events.NewMessage.Event, settings: UserBotSettings
) -> None:
    chat = await event.get_chat()
    chat_id = event.chat_id
    chat_username = _normalize(getattr(chat, "username", None))

    matches_chat = False
    if not settings.target_chat_ids and not settings.target_chat_usernames:
        matches_chat = True
    if settings.target_chat_ids and chat_id in settings.target_chat_ids:
        matches_chat = True
    if settings.target_chat_usernames and chat_username in settings.target_chat_usernames:
        matches_chat = True

    if not matches_chat:
        logger.debug(
            "Skip chat chat_id=%s username=%s", chat_id, chat_username
        )
        return

    sender = await event.get_sender()
    sender_id = event.sender_id
    sender_username = _normalize(getattr(sender, "username", None)) if sender else ""

    sender_filters_defined = bool(
        settings.monitored_user_ids or settings.monitored_user_usernames
    )
    sender_match = True
    if sender_filters_defined:
        sender_match = False
        if sender_id is not None and sender_id in settings.monitored_user_ids:
            sender_match = True
        if sender_username and sender_username in settings.monitored_user_usernames:
            sender_match = True

    if not sender_match:
        logger.debug(
            "Sender did not match filters chat_id=%s message_id=%s sender_id=%s username=%s",
            chat_id,
            event.message.id,
            sender_id,
            sender_username,
        )
        return

    message_text = event.message.message or event.message.raw_text or ""
    if not _matches_any(message_text, settings.match_keywords):
        logger.debug(
            "Message text did not match keywords chat_id=%s message_id=%s",
            chat_id,
            event.message.id,
        )
        return

    logger.info(
        "Scheduling deletion chat_id=%s message_id=%s delay=%ss",
        chat_id,
        event.message.id,
        settings.delete_delay_seconds,
    )

    asyncio.create_task(
        _delete_later(event.client, chat_id, event.message.id, settings.delete_delay_seconds)
    )


async def main() -> None:
    settings = UserBotSettings.from_env()
    logging.basicConfig(level=logging._nameToLevel.get(settings.log_level, logging.INFO))

    client = TelegramClient(
        settings.session_name,
        settings.api_id,
        settings.api_hash,
    )

    await client.start(phone=settings.phone_number)
    me = await client.get_me()
    logger.info(
        "Userbot started as %s (id=%s)",
        getattr(me, "username", None) or getattr(me, "first_name", "unknown"),
        me.id,
    )
    logger.info("Monitoring chats: %s", settings.describe_targets())
    logger.info("Filters: %s", settings.describe_filters())

    @client.on(events.NewMessage)
    async def _listener(event: events.NewMessage.Event) -> None:
        await _handle_event(event, settings)

    logger.info("Userbot is running. Press Ctrl+C to stop.")
    await client.run_until_disconnected()


if __name__ == "__main__":  # pragma: no cover - script use
    asyncio.run(main())
