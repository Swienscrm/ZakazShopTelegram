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

#ТОВАР (обновленная версия с сохранением item_id)
@router.callback_query(F.data.startswith("item_")) 
async def show_item(callback:CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    item_data = await db.get_item(item_id)
    await callback.answer("Вы выбрали товар")
    await callback.message.delete()
    await callback.message.answer(
        f"✨{item_data.name}\n\nОписание:\n{item_data.description}\n\nЦена: {item_data.price}₽", 
        reply_markup=await kb.item(item_data.category, item_id)
    )

# Добавление товара в корзину
@router.callback_query(F.data.startswith("add_item_cart_"))
async def add_to_cart_handler(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[-1])
    tg_id = callback.from_user.id
    
    success = await db.add_to_cart(tg_id, item_id)
    if success:
        await callback.answer("✅ Товар добавлен в корзину!", show_alert=True)
    else:
        await callback.answer("❌ Ошибка при добавлении товара", show_alert=True)

# Обработчик "Корзина" (обновленная версия с отображением товаров)
@router.message(F.text == "Корзина")
async def cart(message:Message):
    await message.delete()
    tg_id = message.from_user.id
    cart_items = await db.get_cart_items(tg_id)
    total = await db.get_cart_total(tg_id)
    
    if not cart_items:
        await message.answer(
            "🛒 Ваша корзина пуста\n\nДобавьте товары из каталога, чтобы они появились здесь.",
            reply_markup=kb.cart
        )
    else:
        cart_text = "🛒 Ваша корзина — Beads Factory\n\n"
        cart_text += "Товары в корзине:\n\n"
        
        for item in cart_items:
            cart_text += f"• {item['name']}\n"
            cart_text += f"  Цена: {item['price']}₽ × {item['quantity']} = {item['total']}₽\n\n"
        
        cart_text += f"💰 Итого: {total}₽\n\n"
        cart_text += "Выберите действие ниже 👇"
        
        await message.answer(cart_text, reply_markup=await kb.cart_items(cart_items))

@router.callback_query(F.data == "back_to_cart")
async def back_to_cart(callback: CallbackQuery):
    await callback.message.delete()
    tg_id = callback.from_user.id
    cart_items = await db.get_cart_items(tg_id)
    total = await db.get_cart_total(tg_id)
    
    if not cart_items:
        await callback.message.answer(
            "🛒 Ваша корзина пуста\n\nДобавьте товары из каталога, чтобы они появились здесь.",
            reply_markup=kb.cart
        )
    else:
        cart_text = "🛒 Ваша корзина — Beads Factory\n\n"
        cart_text += "Товары в корзине:\n\n"
        
        for item in cart_items:
            cart_text += f"• {item['name']}\n"
            cart_text += f"  Цена: {item['price']}₽ × {item['quantity']} = {item['total']}₽\n\n"
        
        cart_text += f"💰 Итого: {total}₽\n\n"
        cart_text += "Выберите действие ниже 👇"
        
        await callback.message.answer(cart_text, reply_markup=await kb.cart_items(cart_items))

# Удаление товара из корзины
@router.callback_query(F.data.startswith("delete_cart_item_"))
async def delete_cart_item_handler(callback: CallbackQuery):
    cart_id = int(callback.data.split("_")[-1])
    tg_id = callback.from_user.id
    
    success = await db.delete_cart_item(tg_id, cart_id)
    if success:
        await callback.answer("✅ Товар удален из корзины", show_alert=True)
        # Обновляем отображение корзины
        await callback.message.delete()
        cart_items = await db.get_cart_items(tg_id)
        total = await db.get_cart_total(tg_id)
        
        if not cart_items:
            await callback.message.answer(
                "🛒 Ваша корзина пуста\n\nДобавьте товары из каталога, чтобы они появились здесь.",
                reply_markup=kb.cart
            )
        else:
            cart_text = "🛒 Ваша корзина — Beads Factory\n\n"
            cart_text += "Товары в корзине:\n\n"
            
            for item in cart_items:
                cart_text += f"• {item['name']}\n"
                cart_text += f"  Цена: {item['price']}₽ × {item['quantity']} = {item['total']}₽\n\n"
            
            cart_text += f"💰 Итого: {total}₽\n\n"
            cart_text += "Выберите действие ниже 👇"
            
            await callback.message.answer(cart_text, reply_markup=await kb.cart_items(cart_items))
    else:
        await callback.answer("❌ Ошибка при удалении товара", show_alert=True)

# Очистка корзины
@router.callback_query(F.data == "clear_cart")
async def clear_cart_handler(callback: CallbackQuery):
    tg_id = callback.from_user.id
    success = await db.clear_cart(tg_id)
    
    if success:
        await callback.answer("✅ Корзина очищена", show_alert=True)
        await callback.message.delete()
        await callback.message.answer(
            "🛒 Ваша корзина пуста\n\nДобавьте товары из каталога, чтобы они появились здесь.",
            reply_markup=kb.cart
        )
    else:
        await callback.answer("❌ Ошибка при очистке корзины", show_alert=True)

# Оформление заказа
@router.callback_query(F.data == "order")
async def order_handler(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cart_items = await db.get_cart_items(tg_id)
    total = await db.get_cart_total(tg_id)
    
    if not cart_items:
        await callback.answer("❌ Ваша корзина пуста", show_alert=True)
        return
    
    # Формируем текст заказа
    order_text = "📦 Оформление заказа\n\n"
    order_text += "Ваш заказ:\n\n"
    
    for item in cart_items:
        order_text += f"• {item['name']} — {item['quantity']} шт. × {item['price']}₽ = {item['total']}₽\n"
    
    order_text += f"\n💰 Итого: {total}₽\n\n"
    order_text += "Для оформления заказа свяжитесь с менеджером:\n"
    order_text += "@wntkkk\n\n"
    order_text += "Или используйте кнопку ниже 👇"
    
    await callback.message.delete()
    await callback.message.answer(order_text, reply_markup=kb.order_keyboard())

# Удаление товаров (старый обработчик - можно оставить для совместимости)
@router.callback_query(F.data == "delete_product")
async def delete_product_handler(callback: CallbackQuery):
    await callback.answer("Используйте кнопки удаления рядом с каждым товаром", show_alert=True)

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