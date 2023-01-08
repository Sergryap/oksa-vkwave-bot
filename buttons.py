from vkwave.bots.utils.keyboards.keyboard import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor
from vkwave.bots import SimpleBotEvent


BTN_DISCOUNT_STEP_4 = [
        'По рекомендации',
        'Через Google',
        'Через Yandex',
        'Нашла в 2Gis',
        'Нашла в ВК',
        'Нашла в Instagram',
    ]

FEEDBACK_BUTTONS = ['Да', 'Нет', 'Скорее да', 'Скорее нет']


def get_button_func():
    return {
        'send_photo': get_button_send_photo,
        'fsm_quiz': get_button_fsm_quiz,
        'fsm_quiz_inline': get_button_fsm_quiz_inline,
        'training_buttons': get_button_training,
        'break': get_button_break,
        'practic_extention': get_practic_extention,
        'what_job': get_what_job,
        'entry_link': get_entry_link,
        'pass': get_button_pass,
        'start': get_start_menu,
        'search': get_search_our,
        'menu': menu,
        'feedback': get_feedback,
        'feedback_assessment': get_feedback_assessment,
        'feedback_continue': get_feedback_continue
    }


def get_main_menu():

    keyboard = Keyboard(one_time=False, inline=False)
    buttons = ['Записаться', '☰ Menu', 'Обучение', 'Примеры работ']
    buttons_color = [
        ButtonColor.PRIMARY,
        ButtonColor.PRIMARY,
        ButtonColor.SECONDARY,
        ButtonColor.SECONDARY
    ]
    for btn, btn_color in zip(buttons[:2], buttons_color[:2]):
        keyboard.add_text_button(btn, btn_color)
    keyboard.add_row()
    for btn, btn_color in zip(buttons[2:], buttons_color[2:]):
        keyboard.add_text_button(btn, btn_color)
    return keyboard.get_keyboard()


def get_start_menu():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = [
        'Записатьcя',
        'Price',
        'Наш адрес',
        'Наши работы',
        'Админ.',
        'Наши курсы',
        'Скидка новичкам'
    ]
    btn_color = ButtonColor.SECONDARY
    btn_finish = ButtonColor.PRIMARY
    for i, btn in enumerate(buttons, start=1):
        if i != len(buttons):
            keyboard.add_text_button(btn, btn_color)
        else:
            keyboard.add_text_button(btn, btn_finish)
        if i != len(buttons) and i % 2 == 0:
            keyboard.add_row()
    keyboard.add_row()
    keyboard.add_text_button('Ваше мнение о нас', payload={'button': 'feedback'})

    return keyboard.get_keyboard()


def get_button_send_photo():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = ['Смoтреть еще', '☰ MENU']
    btn_color = ButtonColor.PRIMARY
    for btn in buttons:
        keyboard.add_text_button(btn, btn_color)
    return keyboard.get_keyboard()


def get_button_fsm_quiz():
    keyboard = Keyboard(one_time=False, inline=False)
    buttons = ['Отмена', 'Пропустить']
    btn_color = ButtonColor.PRIMARY
    for btn in buttons:
        keyboard.add_text_button(btn, btn_color)
    return keyboard.get_keyboard()


def get_button_fsm_quiz_inline():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = ['Пропустить']
    btn_color = ButtonColor.PRIMARY
    for btn in buttons:
        keyboard.add_text_button(btn, btn_color)
    return keyboard.get_keyboard()


def get_button_training():
    keyboard = Keyboard(one_time=False, inline=True)
    keyboard.add_text_button('Заполнить анкету', ButtonColor.PRIMARY)
    keyboard.add_row()
    keyboard.add_text_button('☰ MENU', ButtonColor.SECONDARY)
    return keyboard.get_keyboard()


def get_button_break():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = ['Отменить']
    btn_color = ButtonColor.PRIMARY
    for btn in buttons:
        keyboard.add_text_button(btn, btn_color)
    return keyboard.get_keyboard()


def get_button_pass():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons_color = ButtonColor.PRIMARY
    keyboard.add_text_button('Пропустить', buttons_color)
    return keyboard.get_keyboard()


def get_practic_extention():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = ['Да', 'Нет']
    btn_color = ButtonColor.PRIMARY
    for btn in buttons:
        keyboard.add_text_button(btn, btn_color)
    return keyboard.get_keyboard()


def get_what_job():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = [
        'Работаю в сфере красоты',
        'Медицинский работник',
        'Работаю в другой сфере',
        'Домохозяйка',
        'Учусь',
    ]
    btn_color = ButtonColor.SECONDARY
    for i, btn in enumerate(buttons, start=1):
        keyboard.add_text_button(btn, btn_color)
        if i != len(buttons):
            keyboard.add_row()
    return keyboard.get_keyboard()


def get_entry_link():
    keyboard = Keyboard(one_time=False, inline=True)
    keyboard.add_link_button(text='Запишись ONLINE', link='https://vk.com/app5688600_-142029999/')
    return keyboard.get_keyboard()


def get_search_our():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = BTN_DISCOUNT_STEP_4
    btn_color = ButtonColor.SECONDARY
    for i, btn in enumerate(buttons, start=1):
        keyboard.add_text_button(btn, btn_color)
        if i != len(buttons):
            keyboard.add_row()
    return keyboard.get_keyboard()


def get_feedback():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons = FEEDBACK_BUTTONS
    btn_color = ButtonColor.PRIMARY
    for i, btn in enumerate(buttons, start=1):
        keyboard.add_text_button(btn, btn_color)
        if i % 2 == 0 and i != len(FEEDBACK_BUTTONS):
            keyboard.add_row()
    return keyboard.get_keyboard()


def get_feedback_assessment():
    keyboard = Keyboard(one_time=False, inline=True)
    for i in range(10, 0, -1):
        keyboard.add_text_button(str(i), ButtonColor.SECONDARY)
        if i == 6:
            keyboard.add_row()
    return keyboard.get_keyboard()


def get_feedback_continue():
    keyboard = Keyboard(one_time=False, inline=True)
    keyboard.add_text_button('Пропустить')
    return keyboard.get_keyboard()


def menu():
    keyboard = Keyboard(one_time=False, inline=True)
    buttons_color = ButtonColor.PRIMARY
    keyboard.add_text_button('☰ MENU', buttons_color)
    return keyboard.get_keyboard()

