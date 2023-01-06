from vkwave.bots import SimpleLongPollBot
from environs import Env
from client import client_router


if __name__ == '__main__':
    env = Env()
    env.read_env()
    TOKEN = env('VK_TOKEN')
    GROUP_ID = env('GROUP_ID')
    bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)
    bot.dispatcher.add_router(client_router)
    bot.run_forever()
