import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

load_dotenv()


def init_sentry():
    """
    Инициализация Sentry.
    Если SENTRY_DSN не задан — Sentry не инициализируется (без ошибок).
    """
    dsn = os.getenv("SENTRY_DSN")

    if not dsn:
        print("SENTRY_DSN не задан в .env. Sentry отключён")
        return

    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            LoggingIntegration(level="ERROR", event_level="ERROR"),
        ],
        environment=os.getenv("ENV", "development"),
        traces_sample_rate=1.0,  # 100% запросов будут отслеживаться
        profiles_sample_rate=0.5,  # профилирование производительности
        send_default_pii=False,  # не отправлять личные данные
        attach_stacktrace=True,
        max_breadcrumbs=50,
        debug=False,
    )
    print("Sentry успешно инициализирован")
