import os
import random
import time
from vkwave.bots import SimpleBotEvent
from textwrap import dedent
from messages import send_message, send_hello
from verify import get_verify_func, verify_hello

USER_MSG = []
MAX_SEND_ADMIN_MSG = 5


async def handle_main_menu(event: SimpleBotEvent):
	user_id = event.user_id
	msg = event.text.lower().strip()
	if not os.environ.get(f'{user_id}_FIRST_NAME'):
		api = event.api_ctx
		user_data = (await api.users.get(user_ids=user_id)).response[0]
		os.environ[f'{user_id}_FIRST_NAME'] = user_data.first_name
		os.environ[f'{user_id}_LAST_NAME'] = user_data.last_name
	user_info = {
		'first_name': os.environ[f'{user_id}_FIRST_NAME'],
		'last_name': os.environ[f'{user_id}_LAST_NAME']
	}
	if verify_hello(msg):
		await send_hello(event, user_info)
	for verify_msg, send_msg_func in get_verify_func().items():
		if verify_msg(msg):
			await send_msg_func(event, user_info)

	return 'START'


async def handle_users_reply(event: SimpleBotEvent):
	global USER_MSG
	user_id = event.user_id
	text = f'от https://vk.com/id{user_id}: "{event.text}"'
	USER_MSG.append(text)
	if len(USER_MSG) == MAX_SEND_ADMIN_MSG:
		api = event.api_ctx
		msg_head = f'Сообщения в чате https://vk.com/gim142029999:'
		await api.messages.send(
			random_id=random.randint(0, 1000),
			user_ids=os.environ['ADMIN_IDS'].split(),
			message='\n'.join([msg_head] + USER_MSG)
		)
		USER_MSG = []
	if event.text.lower().strip() in ['start', '/start', 'начать', 'старт']:
		user_state = 'START'
	else:
		user_state = os.environ.get(f'{user_id}_NEXT_STATE', 'START')
	states_functions = {
		'START': handle_main_menu,
	}
	state_handler = states_functions[user_state]
	os.environ[f'{user_id}_NEXT_STATE'] = await state_handler(event)
