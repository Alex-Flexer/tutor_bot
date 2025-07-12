from aiogram.dispatcher.middlewares.base import BaseMiddleware
import logging


class BotLoggingMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

        logging.getLogger('aiogram').setLevel(logging.WARNING)
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.logger.propagate = False

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")

        user_info = (
            f"@{user.username}"
            if user
            else "undefined"
        )

        self.logger.info(f"{event.event_type} from {user_info}")

        return await handler(event, data)
