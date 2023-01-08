import os
import random
from vkwave.bots import SimpleBotEvent
from vkwave.bots.storage.storages import Storage
from vkwave.bots.storage.types import Key
from textwrap import dedent
from messages import (
	send_hello,
	send_discount,
	send_message,
	send_menu,
	send_training,
	send_feedback_start,
)
from verify import (
	get_verify_func,
	verify_hello,
	verify_discount,
	verify_menu,
	verify_fsm_break,
	verify_phone,
	verify_fsm_start,
	verify_training,
)
from buttons import BTN_DISCOUNT_STEP_4, FEEDBACK_BUTTONS

storage = Storage()

USER_MSG = []
MAX_SEND_ADMIN_MSG = 5
CANCELLATION_MESSAGE = 'Вы можете продолжить в любое время. Просто отправьте "получить скидку"'
CANCELLATION_MSG_TR_SURVEY = 'Вы можете продолжить в любое время. Просто отправьте "обучение" или "ed"'
CANCELLATION_FEEDBACK = 'Вы можете продолжить в любое время.'


async def get_initial_data(event: SimpleBotEvent):
	user_id = event.user_id
	msg = event.text.lower().strip()
	user_info = {
		'first_name': await storage.get(Key(f'{user_id}_first_name')),
		'last_name': await storage.get(Key(f'{user_id}_last_name'))
	}
	return user_id, msg, user_info


async def handle_main_menu(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)

	if verify_hello(msg):
		await send_hello(event, user_info)

	if verify_discount(msg):
		await send_discount(event, user_info)
		return 'DISCOUNT_SURVEY_1'
	elif verify_training(msg):
		await send_training(event, user_info)
		return 'TRAINING_SURVEY_1'
	elif event.payload and event.payload['button'] == 'feedback':
		await send_feedback_start(event, user_info)
		return 'FEEDBACK_SURVEY_1'

	for verify_msg, send_msg_func in get_verify_func().items():
		if verify_msg(msg):
			await send_msg_func(event, user_info)

	return 'START'


# далее идут шаги по заполнению анкеты на скидку новичкам
async def handle_discount_step_1(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_start(msg):
		text = f'1. {user_info["first_name"]}, оставьте пожалуйста ваш контактный номер телефона:'
		discount_msg = f'vk: https://vk.com/id{user_id}\n'
		await storage.put(Key(f'{user_id}_discount'), discount_msg)
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_SURVEY_2'
	else:
		if verify_hello(msg):
			await send_hello(event, user_info)

		for verify_msg, send_msg_func in get_verify_func().items():
			if verify_msg(msg):
				await send_msg_func(event, user_info)

		return 'START'


async def handle_discount_step_2(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif not verify_phone(msg):
		text = 'Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_SURVEY_2'
	else:
		discount_msg = await storage.get(Key(f'{user_id}_discount')) + f'phone: {msg}\n'
		await storage.put(Key(f'{user_id}_discount'), discount_msg)
		text = '2. Введите ваше имя'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_SURVEY_3'


async def handle_discount_step_3(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	else:
		discount_msg = await storage.get(Key(f'{user_id}_discount')) + f'name: {msg}\n'
		await storage.put(Key(f'{user_id}_discount'), discount_msg)
		text = '3. Как вы нас нашли? Выберите ниже, либо напишите свой вариант'
		await send_message(event, msg=text, buttons='search')
		return 'DISCOUNT_SURVEY_4'


async def handle_discount_step_4(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [msg.lower() for msg in BTN_DISCOUNT_STEP_4]:
		text = f'''
				{user_info["first_name"]}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты:
				'''
		await send_message(event, msg=dedent(text), buttons='search')
		return 'DISCOUNT_SURVEY_4'
	else:
		discount_msg = await storage.get(Key(f'{user_id}_discount')) + f'search: {msg}\n'
		await storage.put(Key(f'{user_id}_discount'), discount_msg)
		text = '4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.'
		await send_message(event, msg=text, buttons='what_job')
		return 'DISCOUNT_SURVEY_5'


async def handle_discount_step_5(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	else:
		discount_msg = await storage.get(Key(f'{user_id}_discount')) + f'work: {msg}\n'
		await storage.put(Key(f'{user_id}_discount'), discount_msg)
		text = '5. Укажите ваш возраст, либо пропустите данный пункт.'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'DISCOUNT_SURVEY_6'


async def handle_discount_step_6(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MESSAGE}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg == "пропустить" or (msg.isdigit() and 10 < int(msg) < 100):
		discount_msg = await storage.get(Key(f'{user_id}_discount')) + f'age: {msg}'
		await storage.put(Key(f'{user_id}_discount'), discount_msg)
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
			message=msg_head + discount_msg
		)
		await storage.delete(Key(f'{user_id}_discount'))
		return 'START'
	else:
		text = f'''
				{user_info["first_name"]}, укажите правильное значение, или пропустите данный пункт.
				Либо отмените заполнение анкеты.
				'''
		await send_message(event, msg=dedent(text), buttons='fsm_quiz')
		return 'DISCOUNT_SURVEY_6'


# далее идут шаги по заполнению анкеты на обучение
async def handle_training_survey_step_1(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_start(msg):
		text = f'1. {user_info["first_name"]}, оставьте пожалуйста ваш контактный номер телефона:'
		training_survey_msg = f'vk: https://vk.com/id{user_id}\n'
		await storage.put(Key(f'{user_id}_training_survey'), training_survey_msg)
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'TRAINING_SURVEY_2'
	else:
		if verify_hello(msg):
			await send_hello(event, user_info)

		for verify_msg, send_msg_func in get_verify_func().items():
			if verify_msg(msg):
				await send_msg_func(event, user_info)

		return 'START'


async def handle_training_survey_step_2(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MSG_TR_SURVEY}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif not verify_phone(msg):
		text = 'Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'TRAINING_SURVEY_2'
	else:
		training_survey_msg = await storage.get(Key(f'{user_id}_training_survey')) + f'phone: {msg}\n'
		await storage.put(Key(f'{user_id}_training_survey'), training_survey_msg)
		text = '2. Введите ваше имя'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'TRAINING_SURVEY_3'


async def handle_training_survey_step_3(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MSG_TR_SURVEY}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	else:
		training_survey_msg = await storage.get(Key(f'{user_id}_training_survey')) + f'name: {msg}\n'
		await storage.put(Key(f'{user_id}_training_survey'), training_survey_msg)
		text = '3. Вы уже имеете опыт в наращивании ресниц?'
		await send_message(event, msg=text, buttons='practic_extention')
		return 'TRAINING_SURVEY_4'


async def handle_training_survey_step_4(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MSG_TR_SURVEY}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg in ['да', 'нет']:
		training_survey_msg = await storage.get(Key(f'{user_id}_training_survey')) + f'practice: {msg}\n'
		await storage.put(Key(f'{user_id}_training_survey'), training_survey_msg)
		text = '4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.'
		await send_message(event, msg=text, buttons='what_job')
		return 'TRAINING_SURVEY_5'
	else:
		text = f'''
				{user_info["first_name"]}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты.
				Вы уже имеете опыт в наращивании ресниц?
				'''
		await send_message(event, msg=dedent(text), buttons='practic_extention')
		return 'TRAINING_SURVEY_4'


async def handle_training_survey_step_5(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MSG_TR_SURVEY}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	else:
		training_survey_msg = await storage.get(Key(f'{user_id}_training_survey')) + f'work: {msg}\n'
		await storage.put(Key(f'{user_id}_training_survey'), training_survey_msg)
		text = '5. Укажите ваш возраст, либо пропустите данный пункт.'
		await send_message(event, msg=text, buttons='fsm_quiz')
		return 'TRAINING_SURVEY_6'


async def handle_training_survey_step_6(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_MSG_TR_SURVEY}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg == "пропустить" or (msg.isdigit() and 10 < int(msg) < 100):
		training_survey_msg = await storage.get(Key(f'{user_id}_training_survey')) + f'age: {msg}'
		await storage.delete(Key(f'{user_id}_training_survey'))
		api = event.api_ctx
		text = f'''
				Спасибо, {user_info["first_name"]}, мы обязательно свяжемся с вами.
				Сообщим всю необходимую информацию о наших курсах и подберем подходящий Вам вариант.
				'''
		await send_message(event, msg=dedent(text))
		msg_head = f'АНКЕТА НА ОБУЧЕНИЕ:\n'
		await api.messages.send(
			random_id=random.randint(0, 1000),
			user_ids=os.environ['ADMIN_IDS'].split(),
			message=msg_head + training_survey_msg
		)
		return 'START'
	else:
		text = f'''
				{user_info["first_name"]}, укажите правильное значение, или пропустите данный пункт.
				Либо отмените заполнение анкеты.
				'''
		await send_message(event, msg=dedent(text), buttons='fsm_quiz')
		return 'TRAINING_SURVEY_6'


# далее идут шаги по заполнению анкеты отзыва
async def handle_feedback_step_1(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_start(msg):
		text = f'1. {user_info["first_name"]}, Ваш мастер приступил к работе вовремя?'
		feedback_msg = f'vk: https://vk.com/id{user_id}\n'
		await storage.put(Key(f'{user_id}_feedback'), feedback_msg)
		await send_message(event, msg='Ответьте на следующие вопросы, пожалуйста:', buttons='fsm_quiz')
		await send_message(event, msg=text, buttons='feedback')
		return 'FEEDBACK_SURVEY_2'
	else:
		if verify_hello(msg):
			await send_hello(event, user_info)

		for verify_msg, send_msg_func in get_verify_func().items():
			if verify_msg(msg):
				await send_msg_func(event, user_info)

		return 'START'


async def handle_feedback_step_2(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_FEEDBACK}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [i.lower() for i in FEEDBACK_BUTTONS]:
		text = f'''
				{user_info['first_name']}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты.
				1. Ваш мастер приступил к работе вовремя?
				'''
		await send_message(event, msg=dedent(text), buttons='feedback')
		return 'FEEDBACK_SURVEY_2'
	else:
		feedback_msg = await storage.get(Key(f'{user_id}_feedback')) + f'Мастер приступил вовремя: {msg}\n'
		await storage.put(Key(f'{user_id}_feedback'), feedback_msg)
		text = '2. Считаете ли вы, что получили подробную консультацию до оказания услуги?'
		await send_message(event, msg=text, buttons='feedback')
		return 'FEEDBACK_SURVEY_3'


async def handle_feedback_step_3(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_FEEDBACK}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [i.lower() for i in FEEDBACK_BUTTONS]:
		text = f'''
				{user_info['first_name']}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты.
				2. Считаете ли вы, что получили подробную консультацию до оказания услуги?
				'''
		await send_message(event, msg=dedent(text), buttons='feedback')
		return 'FEEDBACK_SURVEY_3'
	else:
		feedback_msg = await storage.get(Key(f'{user_id}_feedback')) + f'Консультация до: {msg}\n'
		await storage.put(Key(f'{user_id}_feedback'), feedback_msg)
		text = '3. Правильно ли ваш мастер понял, что вы хотите?'
		await send_message(event, msg=text, buttons='feedback')
		return 'FEEDBACK_SURVEY_4'


async def handle_feedback_step_4(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_FEEDBACK}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [i.lower() for i in FEEDBACK_BUTTONS]:
		text = f'''
				{user_info['first_name']}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты.
				3. Правильно ли ваш мастер понял, что вы хотите?
				'''
		await send_message(event, msg=dedent(text), buttons='feedback')
		return 'FEEDBACK_SURVEY_4'
	else:
		feedback_msg = await storage.get(Key(f'{user_id}_feedback')) + f'Правильно ли мастер понял: {msg}\n'
		await storage.put(Key(f'{user_id}_feedback'), feedback_msg)
		text = f'''
				4. На сколько ваши ожидания совпали с результатом работы?
				Оцените по шкале от 1 до 10, где:
				10 - полностью совпали
				1 - совсем не то, что ожидала
				'''
		await send_message(event, msg=dedent(text), buttons='feedback_assessment')
		return 'FEEDBACK_SURVEY_5'


async def handle_feedback_step_5(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_FEEDBACK}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [str(i) for i in range(1, 11)]:
		text = f'''
				{user_info['first_name']}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты.
				4. На сколько ваши ожидания совпали с результатом работы?
				Оцените по шкале от 1 до 10, где:
				10 - полностью совпали
				1 - совсем не то, что ожидала
				'''
		await send_message(event, msg=dedent(text), buttons='feedback_assessment')
		return 'FEEDBACK_SURVEY_5'
	else:
		feedback_msg = await storage.get(Key(f'{user_id}_feedback')) + f'Оценка ожидания: {msg}\n'
		await storage.put(Key(f'{user_id}_feedback'), feedback_msg)
		text = '5. Вы планируете посетить наш салон снова?'
		await send_message(event, msg=text, buttons='feedback')
		return 'FEEDBACK_SURVEY_6'


async def handle_feedback_step_6(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_FEEDBACK}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [i.lower() for i in FEEDBACK_BUTTONS]:
		text = f'''
				{user_info['first_name']}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты.
				5. Вы планируете посетить наш салон снова?
				'''
		await send_message(event, msg=dedent(text), buttons='feedback')
		return 'FEEDBACK_SURVEY_6'
	else:
		feedback_msg = await storage.get(Key(f'{user_id}_feedback')) + f'Планирует посетить снова: {msg}\n'
		await storage.put(Key(f'{user_id}_feedback'), feedback_msg)
		text = f'''
				6. {user_info["first_name"]}, порекомендуете ли вы наш салон своим друзьям и близким?
				Оцените по шкале от 1 до 10, где:
				10 - непременно порекомендую
				1 - непременно не порекомендую
				'''
		await send_message(event, msg=dedent(text), buttons='feedback_assessment')
		return 'FEEDBACK_SURVEY_7'


async def handle_feedback_step_7(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_FEEDBACK}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	elif msg not in [str(i) for i in range(1, 11)]:
		text = f'''
				{user_info["first_name"]}, данный пункт обязателен к заполнению.
				Укажите вариант, либо отмените заполнение анкеты.
				6. Порекомендуете ли вы наш салон своим друзьям и близким?
				Оцените по шкале от 1 до 10, где:
				10 - непременно порекомендую
				1 - непременно не порекомендую
				'''
		await send_message(event, msg=dedent(text), buttons='feedback_assessment')
		return 'FEEDBACK_SURVEY_7'
	else:
		feedback_msg = await storage.get(Key(f'{user_id}_feedback')) + f'Вероятность рекомендации: {msg}\n'
		await storage.put(Key(f'{user_id}_feedback'), feedback_msg)
		text = f'''
				{user_info["first_name"]}, Вы можете оставить свои пожелания в произвольной форме.
				Либо пропустите данный пункт
				'''
		await send_message(event, msg=dedent(text), buttons='feedback_continue')
		return 'FEEDBACK_SURVEY_8'


async def handle_feedback_step_8(event: SimpleBotEvent):
	user_id, msg, user_info = await get_initial_data(event)
	if verify_fsm_break(msg):
		text = f'{user_info["first_name"]} {CANCELLATION_FEEDBACK}'
		await send_message(event, msg=text)
		await send_menu(event, user_info)
		return 'START'
	else:
		feedback_msg = await storage.get(Key(f'{user_id}_feedback')) + f'Произвольное: {msg}'
		await storage.delete(Key(f'{user_id}_feedback'))
		api = event.api_ctx
		text = f'''
				Спасибо, {user_info["first_name"]}, за ваши ответы.
				Мы обязательно учтем ваше мнение, чтобы сделать наши услуги еще лучше.
				'''
		await send_message(event, msg=dedent(text))
		msg_head = f'FEEDBACK:\n'
		await api.messages.send(
			random_id=random.randint(0, 1000),
			user_ids=os.environ['ADMIN_IDS'].split(),
			message=msg_head + feedback_msg
		)

		return 'START'


# Общий хэндлер
async def handle_users_reply(event: SimpleBotEvent):
	global USER_MSG
	user_id = event.user_id
	api = event.api_ctx
	if not await storage.contains(Key(f'{user_id}_first_name')):
		user_data = (await api.users.get(user_ids=user_id)).response[0]
		await storage.put(Key(f'{user_id}_first_name'), user_data.first_name)
		await storage.put(Key(f'{user_id}_last_name'), user_data.last_name)

	text = f'от https://vk.com/id{user_id}: "{event.text}"'
	USER_MSG.append(text)
	if len(USER_MSG) == MAX_SEND_ADMIN_MSG:
		msg_head = f'Сообщения в чате https://vk.com/gim{os.environ["GROUP_ID"]}:'
		await api.messages.send(
			random_id=random.randint(0, 1000),
			user_ids=os.environ['ADMIN_IDS'].split(),
			message='\n'.join([msg_head] + USER_MSG)
		)
		USER_MSG = []

	if event.text.lower().strip() in ['start', '/start', 'начать', 'старт']:
		user_state = 'START'
	else:
		user_state = await storage.get(Key(f'{user_id}_next_state'), default='START')
	states_functions = {
		'START': handle_main_menu,
		'DISCOUNT_SURVEY_1': handle_discount_step_1,
		'DISCOUNT_SURVEY_2': handle_discount_step_2,
		'DISCOUNT_SURVEY_3': handle_discount_step_3,
		'DISCOUNT_SURVEY_4': handle_discount_step_4,
		'DISCOUNT_SURVEY_5': handle_discount_step_5,
		'DISCOUNT_SURVEY_6': handle_discount_step_6,
		'TRAINING_SURVEY_1': handle_training_survey_step_1,
		'TRAINING_SURVEY_2': handle_training_survey_step_2,
		'TRAINING_SURVEY_3': handle_training_survey_step_3,
		'TRAINING_SURVEY_4': handle_training_survey_step_4,
		'TRAINING_SURVEY_5': handle_training_survey_step_5,
		'TRAINING_SURVEY_6': handle_training_survey_step_6,
		'FEEDBACK_SURVEY_1': handle_feedback_step_1,
		'FEEDBACK_SURVEY_2': handle_feedback_step_2,
		'FEEDBACK_SURVEY_3': handle_feedback_step_3,
		'FEEDBACK_SURVEY_4': handle_feedback_step_4,
		'FEEDBACK_SURVEY_5': handle_feedback_step_5,
		'FEEDBACK_SURVEY_6': handle_feedback_step_6,
		'FEEDBACK_SURVEY_7': handle_feedback_step_7,
		'FEEDBACK_SURVEY_8': handle_feedback_step_8,
	}
	state_handler = states_functions[user_state]
	await storage.put(Key(f'{user_id}_next_state'), value=await state_handler(event))
