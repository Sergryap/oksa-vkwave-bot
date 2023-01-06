import os

from vkwave.bots import SimpleBotEvent
from textwrap import dedent

from buttons import get_main_menu, get_start_menu


async def msg_handler(event: SimpleBotEvent):
	user_id = event.user_id
	text = event.text
	os.environ[f'{user_id}_NEXT_STATE'] = 'START_MENU'
	msg = '''
	Я чат-бот Oksa-studio.
	Очень рад видеть Вас у нас.
	'''
	await event.answer(
		message=dedent(msg),
		keyboard=get_main_menu()
	)


async def handle_main_menu(event: SimpleBotEvent):
	user_id = event.user_id
	text = event.text
	if text == '☰ Menu':
		msg = 'Выберите ниже:'
		keyboard = get_start_menu()

	else:
		msg = '''
		Я чат-бот Oksa-studio.
		Очень рад видеть Вас у нас.
		'''
		keyboard = get_main_menu()

	os.environ[f'{user_id}_NEXT_STATE'] = 'START_MENU'
	await event.answer(
		message=dedent(msg),
		keyboard=keyboard
	)


async def handle_users_reply(event: SimpleBotEvent):
	user_id = event.user_id
	if event.text.lower().strip() in ['start', '/start']:
		user_state = 'START'
	else:
		user_state = os.environ.get(f'{user_id}_NEXT_STATE', 'START')
	states_functions = {
		'START': msg_handler,
		'START_MENU': handle_main_menu
	}
	state_handler = states_functions[user_state]
	await state_handler(event)
