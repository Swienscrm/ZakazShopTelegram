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
    await callback.message.answer(ms.MENU_MESSAGE, reply_markup=kb.menu)


                                      #Обработчик "Каталог"          
@router.message(F.text == "Каталог")
async def catalog(message:Message):
    await message.delete()
    await message.answer(ms.CATALOG_MESSAGE,reply_markup=kb.catalog)
#Выбор кольца
@router.callback_query(F.data == "rings")
async def rings(callback:CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer("Вы выбрали кольца")
#Выбор браслетов
@router.callback_query(F.data == "bracelets")
async def bracelets(callback:CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer("Вы выбрали браслеты")
#Выбор серьги
@router.callback_query(F.data == "earrings")
async def bracelets(callback:CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer("Вы выбрали серьги")
#Выбор другое
@router.callback_query(F.data == "other")
async def bracelets(callback:CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer("Вы выбрали другое")


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