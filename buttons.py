from vkwave.bots.utils.keyboards.keyboard import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor

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
    return keyboard.get_keyboard()
