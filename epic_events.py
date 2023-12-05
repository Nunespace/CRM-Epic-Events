from controllers.login_manager import AuthenticationAndPermissions
from settings import Base, ENGINE
import sentry_sdk
from sentry_sdk import capture_message
import logging
from sentry_sdk.integrations.logging import LoggingIntegration
from sqlalchemy.sql import text
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def login():
    logging.basicConfig(level=logging.INFO)
    sentry_sdk.init(
        dsn="https://f16713045bb51604e66355f096694966@o4506343489601536.ingest.sentry.io/4506345513811968",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        enable_tracing=True,
        integrations=[
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=logging.INFO,  # Send records as events
            ),
        ],
    )

    Base.metadata.create_all(ENGINE)
    run = AuthenticationAndPermissions()
    run.check_password()
    statement = text("SELECT 'Hello World'")

    with ENGINE.connect() as conn:
        with sentry_sdk.start_transaction(name="testing_sentry"):
            result = conn.execute(statement)


if __name__ == "__main__":
    login()
