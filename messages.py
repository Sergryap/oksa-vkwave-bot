import random
import time
import re
import requests
import verify
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
TIME_OFFSET = 0
DAY_END_TIME = 18
EVENING_END_TIME = 23
MORNING_END_TIME = 11
NIGHT_END_TIME = 6


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
