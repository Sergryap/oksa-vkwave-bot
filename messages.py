import random
import time
import re
import requests
import verify
import os
from typing import Union
from vkwave.bots import SimpleBotEvent
from buttons import get_button_func, get_main_menu, menu
from photos import photos
from textwrap import dedent


COMMAND = f'''
       ✔️ Помочь записатьcя - "z"
       ✔️️ Сориентировать по ценам - "p"
       ✔️️ Наш адрес - "h"
       ✔️️ Показать наши работы - "ex"
       ✔️️ Связаться с администрацией - "ad"
       ✔️️ Про наши курсы - "ed"
       ✔️️ Начать с начала - "start"
       '''

TIME_OFFSET = 5
DAY_END_TIME = 18
EVENING_END_TIME = 23
MORNING_END_TIME = 11
NIGHT_END_TIME = 6


def get_discount_step(user_info):
    return {
        'step_1': {
            'true': f'1. {user_info["first_name"]}, оставьте пожалуйста ваш контактный номер телефона:',
            'false': 'Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты'
        },
        'step_2': {'true': '2. Введите ваше имя'},
        'step_3': {
            'true': '3. Как вы нас нашли? Выберите ниже, либо напишите свой вариант',
            'false': f'''
                {user_info["first_name"]}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты:
                '''
        },
        'step_4': {
            'true': '4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.'
        },
        'step_5': {
            'true': '5. Укажите ваш возраст, либо пропустите данный пункт.',
            'false': f'''
                {user_info["first_name"]}, укажите правильное значение, или пропустите данный пункт.
                Либо отмените заполнение анкеты.
                '''
        },
        'step_6': {
            'true': f'''
                Спасибо, {user_info["first_name"]}, мы обязательно свяжемся с вами.
                Сообщим всю необходимую информацию и подберем удобное время для записи со скидкой.
                '''
        }
    }


def get_training_step(user_info):
    return {
        'step_1': {
            'true': f'1. {user_info["first_name"]}, оставьте пожалуйста ваш контактный номер телефона:',
            'false': 'Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты'
        },
        'step_2': {
            'true': '2. Введите ваше имя'
        },
        'step_3': {
            'true': '3. Вы уже имеете опыт в наращивании ресниц?',
            'false': f'''
                {user_info["first_name"]}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты.
                Вы уже имеете опыт в наращивании ресниц?
                '''
        },
        'step_4': {
            'true': '4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.',
        },
        'step_5': {
            'true': '5. Укажите ваш возраст, либо пропустите данный пункт.',
            'false': f'''
                {user_info["first_name"]}, укажите правильное значение, или пропустите данный пункт.
                Либо отмените заполнение анкеты.
                '''
        },
        'step_6': {
            'true': f'''
                Спасибо, {user_info["first_name"]}, мы обязательно свяжемся с вами.
                Сообщим всю необходимую информацию о наших курсах и подберем подходящий Вам вариант.
                ''',
        },
    }


def get_feedback_step(user_info):
    return {
        'step_1': {
            'true': f'1. {user_info["first_name"]}, Ваш мастер приступил к работе вовремя?',
            'false': f'''
                {user_info['first_name']}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты.
                1. Ваш мастер приступил к работе вовремя?
                '''
        },
        'step_2': {
            'true': '2. Считаете ли вы, что получили подробную консультацию до оказания услуги?',
            'false': f'''
                {user_info['first_name']}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты.
                2. Считаете ли вы, что получили подробную консультацию до оказания услуги?
                '''
        },
        'step_3': {
            'true': '3. Правильно ли ваш мастер понял, что вы хотите?',
            'false': f'''
                {user_info['first_name']}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты.
                3. Правильно ли ваш мастер понял, что вы хотите?
                '''
        },
        'step_4': {
            'true': f'''
                4. На сколько ваши ожидания совпали с результатом работы?
                Оцените по шкале от 1 до 10, где:
                10 - полностью совпали
                1 - совсем не то, что ожидала
                ''',
            'false': f'''
                {user_info['first_name']}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты.
                4. На сколько ваши ожидания совпали с результатом работы?
                Оцените по шкале от 1 до 10, где:
                10 - полностью совпали
                1 - совсем не то, что ожидала
                '''
        },
        'step_5': {
            'true': '5. Вы планируете посетить наш салон снова?',
            'false': f'''
                {user_info['first_name']}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты.
                5. Вы планируете посетить наш салон снова?
                '''
        },
        'step_6': {
            'true': f'''
                6. {user_info["first_name"]}, порекомендуете ли вы наш салон своим друзьям и близким?
                Оцените по шкале от 1 до 10, где:
                10 - непременно порекомендую
                1 - непременно не порекомендую
                ''',
            'false': f'''
                {user_info["first_name"]}, данный пункт обязателен к заполнению.
                Укажите вариант, либо отмените заполнение анкеты.
                6. Порекомендуете ли вы наш салон своим друзьям и близким?
                Оцените по шкале от 1 до 10, где:
                10 - непременно порекомендую
                1 - непременно не порекомендую
                '''
        },
        'step_7': {
            'true': f'''
                {user_info["first_name"]}, Вы можете оставить свои пожелания в произвольной форме.
                Либо пропустите данный пункт
                '''
        },
        'step_8': {
            'true': f'''
                Спасибо, {user_info["first_name"]}, за ваши ответы.
                Мы обязательно учтем ваше мнение, чтобы сделать наши услуги еще лучше.
                '''
        }
    }


async def send_message(
        event: SimpleBotEvent,
        msg: str = None,
        buttons: Union[str, bool] = True,
        lat: int = None,
        long: int = None
):
    """
    Отправка сообщения пользователю.
    Если buttons=True создается клавиатура
    """
    button_func = get_button_func()
    for key, get_buttons in button_func.items():
        if buttons == key:
            keyboard = get_buttons()
            break
        elif buttons:
            keyboard = get_main_menu()
    try:
        if lat and long:
            api = event.api_ctx
            user_id = event.user_id
            await api.messages.send(
                user_id=user_id,
                random_id=random.randint(0, 1000),
                message=msg,
                keyboard=keyboard,
                lat=lat,
                long=long
            )
        else:
            await event.answer(
                message=msg,
                keyboard=keyboard
            )
    except requests.exceptions.ConnectionError:
        time.sleep(1)
        await send_message(event, msg, buttons, lat, long)


def good_time():
    tm = time.ctime()
    pattern = re.compile(r"(\d+):\d+:\d+")
    h = int(pattern.search(tm).group(1))
    h = h + TIME_OFFSET if h + TIME_OFFSET < 24 else (h + TIME_OFFSET) % 24
    if h < NIGHT_END_TIME:
        return "Доброй ночи"
    elif h < MORNING_END_TIME:
        return "Доброе утро"
    elif h < DAY_END_TIME:
        return "Добрый день"
    elif h <= EVENING_END_TIME:
        return "Добрый вечер"


async def send_hello(event: SimpleBotEvent, user_info):

    d = [
        '\nНапишите, что бы вы хотели или выберите.',
        '\nНапишите мне, что вас интересует или выберите.',
        '\nЧто вас интересует? Напишите пожалуйста или выберите.'
    ]

    t = f"""
        Пока менеджеры {'спят' if good_time() == 'Доброй ночи' else 'заняты'} я могу:
        {COMMAND}
        """

    delta = random.choice(d)
    t1 = f"{good_time()}, {user_info['first_name']}!\nЯ бот Oksa-studio.\nБуду рад нашему общению.\n"
    t2 = f"{good_time()}, {user_info['first_name']}!\nЯ чат-бот Oksa-studio.\nОчень рад видеть Вас у нас.\n"
    t3 = f"{good_time()}, {user_info['first_name']}!\nЯ бот этого чата.\nРад видеть Вас у нас в гостях.\n"
    text = random.choice([t1, t2, t3])

    if verify.verify_only_hello(event.text.lower().strip()):
        await send_message(event, msg=text)
        await send_message(event, msg=f'{delta}', buttons='start')
    else:
        await send_message(event, msg=text)


async def send_link_entry(event: SimpleBotEvent, user_info):
    text1 = f"""
             {user_info['first_name']}, узнать о свободных местах, своих записях и/или записаться можно:\n
             ✔️ Самостоятельно: https://dikidi.net/72910
             ✔️ По тел. +7(919)442-35-36
             ✔️ Через личные сообщения: @id9681859 (Оксана)
             ✔ Дождаться сообщения от нашего менеджера
             """
    text2 = "Что вас еще интересует напишите или выберите ниже:"
    await send_message(event, msg=dedent(text1), buttons='entry_link')
    await send_message(event, msg=text2, buttons='menu')
    api = event.api_ctx
    admin_msg = f'Клиент "{user_info["first_name"]}" записывается в чате: https://vk.com/gim{os.environ["GROUP_ID"]}'
    await api.messages.send(
        random_id=random.randint(0, 1000),
        user_ids=os.environ['ADMIN_IDS'].split(),
        message=admin_msg
    )


async def send_price(event: SimpleBotEvent, user_info):
    text = f"""
            {user_info['first_name']}, цены на наши услуги можно посмотреть здесь:
            ✔️ vk.com/uslugi-142029999\n
            """
    text2 = "Что вас еще интересует напишите или выберите ниже:"
    await send_message(event, msg=dedent(text))
    await send_message(event, msg=text2, buttons='start')


async def send_contact_admin(event: SimpleBotEvent, user_info):
    text = f"""
            {user_info['first_name']}, мы обязательно свяжемся с Вами в ближайшее время.
            Кроме того, для связи с руководством Вы можете воспользоваться следующими контактами:
            ✔ https://vk.com/id448564047
            ✔ https://vk.com/id9681859
            ✔ Email: oksarap@mail.ru
            ✔ Тел.: +7(919)442-35-36\n
            """
    text2 = "Что вас еще интересует, напишите или выберите ниже:"
    await send_message(event, msg=dedent(text))
    await send_message(event, msg=text2, buttons='menu')


async def send_site(event: SimpleBotEvent, user_info):
    text = f"""
            {user_info['first_name']}, много полезной информации о наращивании ресниц смотрите на нашем сайте:
            https://oksa-studio.ru/\n
            """
    text2 = "Что вас еще интересует напишите или выберите ниже:"
    await send_message(event, msg=text)
    await send_message(event, msg=text2, buttons='menu')


async def send_address(event: SimpleBotEvent, user_info):
    text1 = f'''
             {user_info['first_name']}, мы находимся по адресу:
             📍 г.Пермь, ул. Тургенева, д. 23.
             '''
    text2 = f'''
             Это малоэтажное кирпичное здание слева от ТЦ "Агат" 
             Вход через "Идеал-Лик", большой стеклянный тамбур
             Что вас еще интересует напишите или выберите ниже.
             '''

    await send_message(
        event,
        msg=dedent(text1),
        lat=58.017794,
        long=56.293045
    )
    await event.answer(
        message=dedent(text2),
        attachment='photo-195118308_457239030',
        keyboard=menu()
    )


async def send_bay_bay(event: SimpleBotEvent, user_info):
    text1 = f'До свидания, {user_info["first_name"]}. Будем рады видеть вас снова!'
    text2 = f'''
             До скорых встреч, {user_info["first_name"]}.
             Было приятно с Вами пообщаться. Ждём вас снова!
             '''
    text3 = f'''
             Всего доброго Вам, {user_info["first_name"]}.
             Надеюсь мы ответили на Ваши вопросы. Ждём вас снова! До скорых встреч.
             '''
    text = random.choice([text1, text2, text3])
    await send_message(event, msg=dedent(text), buttons='menu')


async def send_work_example(event: SimpleBotEvent, user_info, photos_qty=5):
    text = f'''
            {user_info['first_name']}, больше работ здесь:
            vk.com/albums-142029999
            Что вас еще интересует, напишите или выберите ниже.
            '''

    attachment = ''
    for photo in random.sample(photos, photos_qty):
        attachment += f"{photo},"
    await event.answer(attachment=attachment)
    await send_message(event, msg=dedent(text), buttons='send_photo')


async def send_training(event: SimpleBotEvent, user_info):
    text = f'''
            {user_info['first_name']}, получить подробную информацию о предстоящих курсах
            и/или записаться вы можете, заполнив анкету предварительной записи,
            которая вас ни к чему не обязывает.
            '''

    await send_message(event, msg=dedent(text), buttons='training_buttons')


async def send_discount(event: SimpleBotEvent, user_info):
    text = f'''
            {user_info['first_name']}, заполните анкету и получите скидку на первое посещение 15%.
            Скидка доступна только для первой записи в нашу студию.
            Будем рады вас видеть!
            '''

    await send_message(event, msg=dedent(text), buttons='training_buttons')


async def send_menu(event: SimpleBotEvent, user_info):
    text = "Выберите ниже:"
    await send_message(event, msg=text, buttons='start')


async def send_feedback_start(event: SimpleBotEvent, user_info):
    text = f'''
            {user_info['first_name']}, были у нас на услуге?
            Оставьте свое мнение, заполните анкету ниже.
            Мы обязательно учтем ваши пожелания, чтобы сделать наш сервис еще лучше.
            '''
    await send_message(event, msg=dedent(text), buttons='training_buttons')

