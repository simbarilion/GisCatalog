import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

load_dotenv()


def init_sentry():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            LoggingIntegration(level="ERROR", event_level="ERROR"),
        ],
        environment=os.getenv("ENV", "development"),
        traces_sample_rate=1.0,  # 100% запросов будут отслеживаться
        profiles_sample_rate=0.8,  # профилирование производительности
        send_default_pii=False,  # не отправлять личные данные
        attach_stacktrace=True,
        max_breadcrumbs=50,
    )
