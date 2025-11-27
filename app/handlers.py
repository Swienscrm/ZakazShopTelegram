from aiogram.methods import delete_message
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import F, Router

import app.keyboards as kb
import app.database.requests as db

import app.bot_message as ms
router = Router()


                                     #Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.set_user(message.from_user.id)
    await message.answer(ms.START_MESSAGE, reply_markup=kb.start_menu)


                                      #Главное меню
@router.callback_query((F.data == "startbot") | (F.data == "back_to_menu"))
async def menu(callback:CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы переходите в главное меню")
    await callback.message.answer(ms.MENU_MESSAGE, reply_markup = kb.inline_menu)
    await callback.message.answer("👇 Используйте кнопки ниже для навигации", reply_markup = kb.reply_menu)


                                      #Обработчик "Каталог"          
@router.message(F.text == "Каталог")
async def catalog(message:Message):
    await message.answer(ms.CATALOG_MESSAGE, reply_markup=await kb.categories())
@router.callback_query(F.data == "back_to_categories")
async def catalog(callback:CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(ms.CATALOG_MESSAGE, reply_markup=await kb.categories())

#КАТЕГОРИИ 
@router.callback_query((F.data.startswith("category_")) | (F.data.startswith("back_to_items_")))
async def category(callback:CallbackQuery):
    await callback.answer("вы выбрали категорию")
    if callback.data.startswith("category_"):
        category_id = int(callback.data.split("_")[1])
    else:
        category_id = int(callback.data.split("_")[-1])
    await callback.message.delete()
    await callback.message.answer("Выберите товар по категории", reply_markup=await kb.items(category_id))

#ТОВАР
@router.callback_query(F.data.startswith("item_")) 
async def category(callback:CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    item_data = await db.get_item(item_id)
    await callback.answer("Вы выбрали товар")
    await callback.message.delete()
    await callback.message.answer(f"✨{item_data.name}\n\nОписание:\n{item_data.description}\n\nЦена: {item_data.price}₽", reply_markup=await kb.item(item_data.category))


                                    #Обработчик "Корзина"
@router.message(F.text == "Корзина")
async def cart(message:Message):
    await message.delete()
    await message.answer(ms.CART_MESSAGE, reply_markup=kb.cart)


                                    #Обработчик "Связаться с менеджером"
@router.message(F.text == "Связаться с менеджером")
async def manager(message:Message):
    await message.delete()
    await message.answer(ms.MANAGER_MESSAGE, reply_markup=kb.manager)


                                    #FAQ
@router.message(F.text == "FAQ")
async def manager(message:Message):
    await message.delete()
    await message.answer(ms.FAQ_MESSAGE, reply_markup=kb.faq)