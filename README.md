# Telegram Userbot Cleaner

Лёгкий проект для запуска Telethon-юзербота, который отслеживает выбранные чаты и удаляет сообщения по заданным фильтрам.

## Быстрый старт

1. Скопируйте `.env.example` в `.env` и заполните значения `USERBOT_…`.
2. Установите зависимости: `pip install -r requirements.txt`.
3. Запустите юзербота: `python -m userbot.cleaner`.

При первом запуске Telethon запросит ваш номер телефона и код подтверждения. После успешной авторизации появится файл сессии (`<USERBOT_SESSION_NAME>.session`).

## Конфигурация `.env`

- `USERBOT_API_ID` и `USERBOT_API_HASH` — выдаются на <https://my.telegram.org>.
- `USERBOT_SESSION_NAME` — имя для локального файла сессии (по умолчанию `userbot_session`).
- `USERBOT_PHONE_NUMBER` — можно оставить пустым, чтобы вводить номер вручную.
- `USERBOT_TARGET_CHAT_IDS` — ID групп/каналов (формат `-100…`).
- `USERBOT_TARGET_CHAT_USERNAMES` — публичные username чатов без `@`.
- `USERBOT_MONITORED_USER_IDS` / `USERBOT_MONITORED_USERNAMES` — отправители, чьи сообщения нужно удалять.
- `USERBOT_MATCH_KEYWORDS` — ключевые слова или подстроки для фильтрации сообщений.
- `USERBOT_DELETE_DELAY_SECONDS` — задержка перед удалением сообщения.
- `USERBOT_LOG_LEVEL` — уровень логгирования (`INFO`, `DEBUG` и др.).

Можно комбинировать фильтры: сообщения будут удаляться только если подходят по чату, отправителю (если задан) и ключевым словам (если указаны).

## Структура проекта

```
.
├── .env.example          # шаблон настроек окружения
├── README.md             # описание проекта
├── requirements.txt      # зависимости Telethon-юзербота
└── userbot/
    ├── __init__.py
    ├── cleaner.py        # основной скрипт очищающего юзербота
    └── config.py         # парсинг переменных окружения
```

## Запуск и остановка

- `python -m userbot.cleaner` — запуск юзербота. Возврат в консоль по `Ctrl+C`.
- При изменении фильтров или целевых чатов остановите юзербота и запустите его снова.

Храните `api_hash`, `api_id`, `.env` и файл сессии в надёжном месте.
