# Telegram Userbot Cleaner

Лёгкий проект для запуска Telethon-юзербота, который отслеживает выбранные чаты и удаляет сообщения по заданным фильтрам.

## Быстрый старт (локально)

1. Скопируйте `.env.example` в `.env` и заполните значения `USERBOT_…`.
2. Установите зависимости: `pip install -r requirements.txt`.
3. Запустите юзербота: `python -m userbot.cleaner`.

При первом запуске Telethon запросит номер телефона и код подтверждения. После успешной авторизации появится файл сессии (`<USERBOT_SESSION_NAME>.session`).

## Запуск в Docker

1. Подготовьте файл `.env` в корне проекта (формат описан ниже).
2. Соберите образ: `docker build -t userbot-cleaner .`
3. Запустите контейнер, пробросив `.env` и директорию для хранения сессии:
   ```bash
   docker run --rm \
       --env-file .env \
       -v "$(pwd)/sessions:/app/sessions" \
       userbot-cleaner
   ```
   Папка `sessions/` нужна, чтобы Telethon сохранял файл сессии между перезапусками. Можно изменить путь или использовать bind-монтаж `.`, если нужно хранить файл рядом с исходниками.
   Альтернатива — используйте Docker Compose (файл `docker-compose.yml` уже в проекте):
   ```bash
   docker compose up --build
   ```
   Для запуска через compose с интерактивным вводом кода авторизации выполните сначала:
   ```bash
   docker compose run --rm -it userbot
   ```
   Telethon запросит код, после чего сохранит сессию (по умолчанию в `sessions/`). Дальше можно поднимать сервис обычной командой `docker compose up -d`. Для остановки нажмите `Ctrl+C` или выполните `docker compose down` отдельной командой.
4. Остановка — `Ctrl+C` (если контейнер запущен в foreground) или `docker stop <container>`.

## Конфигурация `.env`

- `USERBOT_API_ID` и `USERBOT_API_HASH` — выдаются на <https://my.telegram.org>.
- `USERBOT_SESSION_NAME` — имя для файла сессии (по умолчанию `userbot_session`). Если запускаетесь в Docker, учтите путь монтирования.
- `USERBOT_PHONE_NUMBER` — можно оставить пустым, чтобы вводить номер вручную.
- `USERBOT_TARGET_CHAT_IDS` — ID групп/каналов (формат `-100…`).
- `USERBOT_TARGET_CHAT_USERNAMES` — публичные username чатов без `@`.
- `USERBOT_MONITORED_USER_IDS` / `USERBOT_MONITORED_USERNAMES` — отправители, чьи сообщения нужно удалять.
- `USERBOT_MATCH_KEYWORDS` — ключевые слова или подстроки для фильтрации сообщений.
- `USERBOT_DELETE_DELAY_SECONDS` — задержка перед удалением сообщения.
- `USERBOT_LOG_LEVEL` — уровень логов (`INFO`, `DEBUG` и др.).

Сообщение удаляется только если совпадает по чату, отправителю (если задан) и ключевым словам (если указаны).

## Структура проекта

```
.
├── .dockerignore         # исключения при сборке docker-образа
├── .env.example          # шаблон настроек окружения
├── .gitignore            # исключения Git
├── Dockerfile            # образ для запуска юзербота
├── README.md             # описание проекта
├── requirements.txt      # зависимости Telethon-юзербота
└── userbot/
    ├── __init__.py
    ├── __main__.py       # позволяет запускать `python -m userbot`
    ├── cleaner.py        # основной скрипт очищающего юзербота
    └── config.py         # парсинг переменных окружения
```

## Запуск и остановка

- `python -m userbot.cleaner` или `python -m userbot` — локальный запуск.
- `docker run … userbot-cleaner` — запуск в контейнере (см. выше).
- При изменении фильтров или целевых чатов остановите юзербота и запустите снова.

Храните `api_hash`, `api_id`, `.env` и файл сессии в надёжном месте. Не коммитьте эти данные в репозиторий.
