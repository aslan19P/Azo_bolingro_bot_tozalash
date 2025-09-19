"""Entry point for running the userbot with `python -m userbot`."""

from __future__ import annotations

import asyncio

from .cleaner import main


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":  # pragma: no cover - script use
    run()
