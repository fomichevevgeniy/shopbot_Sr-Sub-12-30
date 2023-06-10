from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db


def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    order = KeyboardButton(text='🛍 Заказать')
    my_orders = KeyboardButton(text='📖 Мои заказы')
    filials = KeyboardButton(text='🍕 Наши филиалы')
    feedback = KeyboardButton(text='☎ Обратная связь')
    settings = KeyboardButton(text='⚙ Настройки')
    markup.row(order)
    markup.row(my_orders, filials)
    markup.row(feedback, settings)
    return markup


def generate_delivery_type():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    delivery = KeyboardButton(text='🚗 Доставка')
    self_delivery = KeyboardButton(text='🏃 Самовывоз')
    back_btn = KeyboardButton(text='◀ Главное меню')
    markup.row(delivery, self_delivery)
    markup.row(back_btn)
    return markup


def generate_filials():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_btn = KeyboardButton(text='◀ К выбору доставки')
    filials = db.get_filials() # [(Максимка), (Чорсу)]
    buttons = []
    for filial in filials: # (максимка)
        btn = KeyboardButton(text=filial[0])
        buttons.append(btn)
    markup.add(back_btn)
    markup.add(*buttons)
    return markup
