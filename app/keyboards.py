
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, inline_keyboard_button
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item


start_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти к покупкам", callback_data="startbot")]])

reply_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Каталог"),
    KeyboardButton(text="Корзина")],
    [KeyboardButton(text="Связаться с менеджером"),
    KeyboardButton(text="FAQ")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню....")

inline_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⭐ Отзывы клиентов", url="https://t.me/+3sUd12FqwxliYWY6")]])

#Создание клавиш (КАТЕГОРИИ) с помощью БД
async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_to_menu"))
    return keyboard.adjust(2).as_markup()
#Создание клавиш(ТОВАРЫ) с помощью БД
async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_to_categories"))
    return keyboard.adjust(2).as_markup()
#Создание клавиш для товара
async def item(category_id, item_id):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить в корзину", callback_data="add_item_cart")],
        [InlineKeyboardButton(text="🔙Назад",callback_data=f"back_to_items_{category_id}")]])


#Корзина
async def cart_items(cart_items_data):
    keyboard = InlineKeyboardBuilder

    if not cart_items_data:
        keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
        return keyboard.as_markup
    
    for item in cart_items_data:
        keyboard.add(InlineKeyboardButton(
            text=f"хуй{item["name"]} (x{item["quantity"]})",
            callback_data=f"delete_cart_item_{item["cart_id"]}"
        ))
    keyboard.adjust(1)
    keyboard.row(
        InlineKeyboardButton(text = "Оформить заказ", callback_data="order"),
        InlineKeyboardButton(text = "Очистить корзину", callback_data="clear_cart")
        )
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
    return keyboard.as_markup()
manager = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙Назад", callback_data="back_to_menu")]])

faq = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙Назад", callback_data="back_to_menu")]])
