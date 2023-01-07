import re
import messages
from buttons import BTN_DISCOUNT_STEP_4


def get_verify_func():
    return {
        verify_address: messages.send_address,
        verify_entry: messages.send_link_entry,
        verify_price: messages.send_price,
        verify_contact_admin: messages.send_contact_admin,
        verify_thank_you: messages.send_bay_bay,
        verify_our_site: messages.send_site,
        verify_work_example: messages.send_work_example,
        verify_training: messages.send_training,
        verify_discount: messages.send_discount,
        verify_menu: messages.send_menu,
    }


def verify_hello(msg):
    """Проверка сообщения на приветствие"""
    pattern = re.compile(r'\b(?:приве?т|здрав?ств?уй|добрый|доброго\s*времени|рад[а?]\s*видеть|start|старт|начать)\w*')
    return bool(pattern.findall(msg))


def verify_menu(msg):
    """Проверка сообщения на приветствие"""
    pattern = re.compile(r'\b(?:меню|menu)\w*')
    return bool(pattern.findall(msg))


def verify_only_hello(msg):
    """Проверка на то, что пользователь отправил только приветствие"""
    verify_all = bool(
        verify_entry(msg) or
        verify_price(msg) or
        verify_contact_admin(msg) or
        verify_address(msg) or
        verify_our_site(msg)
    )
    return bool(verify_hello(msg) and not verify_all)


def verify_entry(msg):
    """Проверка сообщения на вхождение запроса о записи на услугу"""
    pattern = re.compile(r'\b(?:запис|окош|окн[ао]|свобод|хочу\s*нар[ао]стить)\w*')
    return bool(pattern.findall(msg) or msg == 'z')


def verify_price(msg):
    """Проверка сообщения на запрос прайса на услуги"""
    pattern = re.compile(r'\b(?:прайс|цен[аы]|стоит|стоимост|price)\w*')
    return bool(pattern.findall(msg) or msg == 'p' or msg == 'р')


def verify_contact_admin(msg):
    """Проверка сообщения на запрос связи с администратором"""
    pattern = re.compile(r'\b(?:админ|руковод|директор|начальств|начальник)\w*')
    return bool(pattern.findall(msg) or msg == 'ad')


def verify_address(msg):
    pattern = re.compile(r'\b(?:адрес|вас\s*найти|найти\s*вас|находитесь|добрать?ся|контакты|где\s*ваш\s*офис)\w*')
    return bool(pattern.findall(msg) or msg == 'h')


def verify_work_example(msg):
    pattern = re.compile(
        r'\b(?:примеры?\s*рабо?т|посмотреть\s*рабо?ты|ваших?\s*рабо?ты?|качество\s*рабо?т|наши работы|смoтреть еще)\w*'
    )
    return bool(pattern.findall(msg) or msg == 'ex')


def verify_thank_you(msg):
    pattern = re.compile(r'\b(?:спасибо|спс|благодар|до\s*свидан|пока)\w*')
    return bool(pattern.findall(msg))


def verify_our_site(msg):
    return bool(msg == 'наш сайт' or msg == 'site')


def verify_training(msg, msg_previous=None):
    pattern = re.compile(r'\b(?:обучен|обучить?ся|выучить?ся|научить?ся|курс)\w*')
    if msg_previous:
        return bool(pattern.findall(msg_previous) or msg_previous == 'ed')
    return bool(pattern.findall(msg) or msg == 'ed')


def verify_fsm_quiz_on(msg, fsm_quiz=None):
    pattern_on = re.compile(r'\b(?:анкета|заполнить анкету)\w*')
    pattern_off = re.compile(r'\b(?:отмена|отменить|стоп|stop)\w*')
    if fsm_quiz:
        return bool(pattern_on.findall(msg) and not fsm_quiz)
    else:
        return bool(pattern_off.findall(msg) and fsm_quiz)


def verify_fsm_start(msg):
    pattern = re.compile(r'\b(?:анкета|заполнить анкету)\w*')
    return bool(pattern.findall(msg))


def verify_fsm_break(msg):
    pattern = re.compile(r'\b(?:отмена|отменить|стоп|stop)\w*')
    return bool(pattern.findall(msg))


def verify_phone(msg):
    pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')
    return bool(pattern.findall(msg))


def verify_discount(msg, msg_previous=None):
    pattern = re.compile(r'\b(?:получить скидку|хочу скидку|скидка при первом посещении|скидка новичкам)\w*')
    if msg_previous:
        return bool(pattern.findall(msg_previous) or msg_previous == 'discount')
    return bool(pattern.findall(msg) or msg == 'discount')


if __name__ == '__main__':
    print(verify_entry('записаться'))
