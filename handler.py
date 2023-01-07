import os
import random
from vkwave.bots import SimpleBotEvent
from textwrap import dedent
from messages import send_hello, send_discount, send_message, send_menu
from verify import get_verify_func, verify_hello, verify_discount, verify_menu, verify_fsm_break, verify_phone
from verify import verify_fsm_start
from buttons import BTN_DISCOUNT_STEP_4

USER_MSG = []
MAX_SEND_ADMIN_MSG = 5
CANCELLATION_MESSAGE = 'Вы можете продолжить в любое время. Просто отправьте "получить скидку"'


def get_initial_data(event: SimpleBotEvent):
	user_id = event.user_id
	msg = event.text.lower().strip()
	user_info = {
		'first_name': os.environ[f'{user_id}_FIRST_NAME'],
		'last_name': os.environ[f'{user_id}_LAST_NAME']
	}
	return user_id, msg, user_info


async def handle_main_menu(event: SimpleBotEvent):
	user_id, msg, user_info = get_initial_data(event)

	if verify_hello(msg):
		await send_hello(event, user_info)

	if verify_discount(msg):
		await send_discount(event, user_info)
		return 'DISCOUNT_1'

	for verify_msg, send_msg_func in get_verify_func().items():
		if verify_msg(msg):
			await send_msg_func(event, user_info)

	return 'START'


async def handle_discount_step_1(event: SimpleBotEvent):
	user_id, msg, user_info = get_initial_data(event)
	if verify_fsm_start(msg):
		text = f'1. {user_info["first_name"]}, оставьте пожалуйста ваш контактный номер телефона:'
		os.environ[f'{user_id}_DISCOUNT'] = f'vk: https://vk.com/id{user_id}\n'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_2'
	else:
		if verify_hello(msg):
			await send_hello(event, user_info)

		for verify_msg, send_msg_func in get_verify_func().items():
			if verify_msg(msg):
				await send_msg_func(event, user_info)

		return 'START'


async def handle_discount_step_2(event: SimpleBotEvent):
	user_id, msg, user_info = get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif not verify_phone(msg):
		text = 'Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_2'
	else:
		os.environ[f'{user_id}_DISCOUNT'] += f'phone: {msg}\n'
		text = '2. Введите ваше имя'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_3'


async def handle_discount_step_3(event: SimpleBotEvent):
	user_id, msg, user_info = get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	else:
		os.environ[f'{user_id}_DISCOUNT'] += f'name: {msg}\n'
		text = '3. Как вы нас нашли? Выберите ниже, либо напишите свой вариант'
		await send_message(event, msg=text, buttons='search')
		return 'DISCOUNT_4'


async def handle_discount_step_4(event: SimpleBotEvent):
	user_id, msg, user_info = get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [msg.lower() for msg in BTN_DISCOUNT_STEP_4]:
		text = f'{user_info["first_name"]}, данный пункт обязателен к заполнению. Укажите вариант, либо отмените заполнение анкеты'
		await send_message(event, msg=text, buttons='search')
		return 'DISCOUNT_4'
	else:
		os.environ[f'{user_id}_DISCOUNT'] += f'search: {msg}\n'
		text = '4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.'
		await send_message(event, msg=text, buttons='what_job')
		return 'DISCOUNT_5'


async def handle_discount_step_5(event: SimpleBotEvent):
	user_id, msg, user_info = get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	else:
		os.environ[f'{user_id}_DISCOUNT'] += f'work: {msg}\n'
		text = '5. Укажите ваш возраст, либо пропустите данный пункт.'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_6'


async def handle_discount_step_6(event: SimpleBotEvent):
	user_id, msg, user_info = get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg == "пропустить" or (msg.isdigit() and 10 < int(msg) < 100):
		os.environ[f'{user_id}_DISCOUNT'] += f'age: {msg}'
		api = event.api_ctx
		text = f'''
				Спасибо, {user_info["first_name"]}, мы обязательно свяжемся с вами.
				Сообщим всю необходимую информацию и подберем удобное время для записи со скидкой.
				'''
		await send_message(event, msg=dedent(text))
		msg_head = f'АНКЕТА НА СКИДКУ:\n'
		await api.messages.send(
			random_id=random.randint(0, 1000),
			user_ids=os.environ['ADMIN_IDS'].split(),
			message=msg_head + os.environ[f'{user_id}_DISCOUNT']
		)
		del os.environ[f'{user_id}_DISCOUNT']
		return 'START'
	else:
		text = f'''
				{user_info["first_name"]}, укажите правильное значение, или пропустите данный пункт.
				Либо отмените заполнение анкеты.
				'''
		await send_message(event, msg=dedent(text), buttons='fsm_quiz')
		return 'DISCOUNT_6'


async def handle_users_reply(event: SimpleBotEvent):
	global USER_MSG
	user_id = event.user_id
	api = event.api_ctx

	if not os.environ.get(f'{user_id}_FIRST_NAME'):
		user_data = (await api.users.get(user_ids=user_id)).response[0]
		os.environ[f'{user_id}_FIRST_NAME'] = user_data.first_name
		os.environ[f'{user_id}_LAST_NAME'] = user_data.last_name

	text = f'от https://vk.com/id{user_id}: "{event.text}"'
	USER_MSG.append(text)

	if len(USER_MSG) == MAX_SEND_ADMIN_MSG:
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
		'DISCOUNT_1': handle_discount_step_1,
		'DISCOUNT_2': handle_discount_step_2,
		'DISCOUNT_3': handle_discount_step_3,
		'DISCOUNT_4': handle_discount_step_4,
		'DISCOUNT_5': handle_discount_step_5,
		'DISCOUNT_6': handle_discount_step_6,
	}
	state_handler = states_functions[user_state]
	os.environ[f'{user_id}_NEXT_STATE'] = await state_handler(event)
