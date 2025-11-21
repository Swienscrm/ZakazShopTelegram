
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, inline_keyboard_button



start_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти к покупкам", callback_data="startbot")]])

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Каталог"),
    KeyboardButton(text="Корзина")],
    [KeyboardButton(text="Связаться с менеджером"),
    KeyboardButton(text="FAQ")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню....")


catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Кольца", callback_data="rings"),
    InlineKeyboardButton(text="Браслеты", callback_data="bracelets")],
    [InlineKeyboardButton(text="Серьги", callback_data="earrings"),
    InlineKeyboardButton(text="Другое", callback_data="other")],
    [InlineKeyboardButton(text="🔙Назад", callback_data="back_to_menu")]])


cart = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Оформить заказ", callback_data="order"),
    InlineKeyboardButton(text="Удалить товары", callback_data="delete_product")],
    [InlineKeyboardButton(text="🔙Назад",callback_data="back_to_menu")]])

manager = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙Назад", callback_data="back_to_menu")]])

faq = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙Назад", callback_data="back_to_menu")]])
