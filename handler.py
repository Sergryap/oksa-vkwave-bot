import os
from vkwave.bots import SimpleBotEvent
from textwrap import dedent
from messages import send_message


async def start_handler(event: SimpleBotEvent):
	user_id = event.user_id
	text = event.text
	os.environ[f'{user_id}_NEXT_STATE'] = 'START_MENU'
	msg = '''
			Я чат-бот Oksa-studio.
			Очень рад видеть Вас у нас.
			Напишите, что бы вы хотели или выберите ниже.
			'''
	await send_message(event, dedent(msg))
	await send_message(event, msg='Выберите:', buttons='start')


async def handle_main_menu(event: SimpleBotEvent):
	user_id = event.user_id
	text = event.text
	if text == '☰ Menu':
		msg = 'Выберите:'
		buttons = 'start'

	else:
		msg = '''
				Я чат-бот Oksa-studio.
				Очень рад видеть Вас у нас.
				Напишите, что бы вы хотели или выберите ниже.
				'''
		buttons = 'start'

	os.environ[f'{user_id}_NEXT_STATE'] = 'START_MENU'
	await send_message(event, dedent(msg), buttons)


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
