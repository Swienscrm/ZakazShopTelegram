from app.database.models import Cart, async_session
from app.database.models import User, Category, Item
from sqlalchemy import delete, select, update

                    #Добавление telegram id в БД
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

                    #Вывод категорий(клавиши) из ББ
async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result.all()
                    #Вывод товаров(клавиши) из БД
async def get_category_item(category_id):
    async with async_session() as session:
        result = await session.scalars(select(Item).where(Item.category == category_id))
        return result.all()
                    #Вывод товара(название, описание, цена)в виде сообщния из БД
async def get_item(item_id):
    async with async_session() as session:
        result = await session.scalar(select(Item).where(Item.id == item_id))
        return result
#ККОРЗИНГАААААААААААААААААААААААААААААААААААААААААААААА
# Получение user_id по tg_id
async def get_user_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.id if user else None

# Добавление товара в корзину (обновленная версия с tg_id)
async def add_to_cart(tg_id: int, item_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return False
        
        result = await session.scalar(select(Cart).where(Cart.user_id == user.id, Cart.item_id == item_id))
        if result:
            result.quantity += 1
        else:
            new_item = Cart(user_id=user.id, item_id=item_id, quantity=1)
            session.add(new_item)
        await session.commit()
        return True

# Получение всех товаров из корзины пользователя (ИСПРАВЛЕНО)
async def get_cart_items(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return []
        
        # Правильный синтаксис для join в SQLAlchemy 2.0
        result = await session.execute(
            select(Cart, Item)
            .join(Item, Cart.item_id == Item.id)
            .where(Cart.user_id == user.id)
        )
        cart_items = []
        for cart, item in result.all():
            cart_items.append({
                'cart_id': cart.id,
                'item_id': item.id,
                'name': item.name,
                'price': item.price,
                'quantity': cart.quantity,
                'total': item.price * cart.quantity
            })
        return cart_items

# Получение общей суммы корзины (ИСПРАВЛЕНО)
async def get_cart_total(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return 0
        
        # Правильный синтаксис для join в SQLAlchemy 2.0
        result = await session.execute(
            select(Cart, Item)
            .join(Item, Cart.item_id == Item.id)
            .where(Cart.user_id == user.id)
        )
        total = 0
        for cart, item in result.all():
            total += item.price * cart.quantity
        return total

# Удаление товара из корзины
async def delete_cart_item(tg_id: int, cart_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return False
        
        cart_item = await session.scalar(select(Cart).where(Cart.id == cart_id, Cart.user_id == user.id))
        if cart_item:
            await session.delete(cart_item)
            await session.commit()
            return True
        return False

# Очистка всей корзины
async def clear_cart(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return False
        
        await session.execute(delete(Cart).where(Cart.user_id == user.id))
        await session.commit()
        return True