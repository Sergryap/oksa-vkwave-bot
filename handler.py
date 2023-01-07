import os
from vkwave.bots import SimpleBotEvent
from textwrap import dedent
from messages import send_message, send_hello
from verify import get_verify_func, verify_hello


async def start_handler(event: SimpleBotEvent):
	user_id = event.user_id
	os.environ[f'{user_id}_NEXT_STATE'] = 'START_MENU'
	msg = event.text.lower().strip()
	api = event.api_ctx
	user_data = (await api.users.get(user_ids=user_id)).response[0]
	user_info = {'first_name': user_data.first_name}
	if verify_hello(msg):
		await send_hello(event, user_info)
	for verify, func in get_verify_func().items():
		if verify(msg):
			await func(event, user_info)


async def handle_main_menu(event: SimpleBotEvent):
	user_id = event.user_id
	os.environ[f'{user_id}_NEXT_STATE'] = 'START_MENU'
	msg = event.text.lower().strip()
	api = event.api_ctx
	user_data = (await api.users.get(user_ids=user_id, fields='country,city,bdate,sex')).response[0]
	user_info = {
		'user_id': user_id,
		'city_id': None if not user_data.city else user_data.city.id,
		'first_name': user_data.first_name,
		'last_name': user_data.last_name,
		'bdate': user_data.bdate,
	}
	if verify_hello(msg):
		await send_hello(event, user_info)
	for verify, func in get_verify_func().items():
		if verify(msg):
			await func(event, user_info)


async def handle_users_reply(event: SimpleBotEvent):
	user_id = event.user_id
	if event.text.lower().strip() in ['start', '/start', 'начать', 'старт']:
		user_state = 'START'
	else:
		user_state = os.environ.get(f'{user_id}_NEXT_STATE', 'START')
	states_functions = {
		'START': start_handler,
		'START_MENU': handle_main_menu
	}
	state_handler = states_functions[user_state]
	await state_handler(event)
