from vkwave.bots import (
    SimpleBotEvent,
    SimpleLongPollBot,
    DefaultRouter,
    simple_bot_message_handler
)
from environs import Env
from handler import handle_users_reply
from mat_filter import MatFilter


client_router = DefaultRouter()


@simple_bot_message_handler(client_router, MatFilter())
async def basic_send(event: SimpleBotEvent):
    await handle_users_reply(event)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    TOKEN = env('VK_TOKEN')
    GROUP_ID = env('GROUP_ID')
    bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)
    bot.dispatcher.add_router(client_router)
    bot.run_forever()
