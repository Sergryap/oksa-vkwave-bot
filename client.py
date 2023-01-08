from vkwave.bots import simple_bot_message_handler, simple_bot_handler, SimpleBotEvent, DefaultRouter, TextFilter
from handler import handle_users_reply
from vkwave.bots.core.dispatching.filters import base
from mat_filter import MatFilter

client_router = DefaultRouter()


@simple_bot_message_handler(client_router, MatFilter())
async def basic_send(event: SimpleBotEvent):
	await handle_users_reply(event)
