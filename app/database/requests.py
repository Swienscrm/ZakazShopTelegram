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
async def add_to_cart(user_id:int, item_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Cart).where(Cart.user_id==user_id,Cart.item_id == item_id)   )
        if result:
            result.quantity +=1
        else:
            new_item = Cart(user_id=user_id,item_id=item_id,quantity=1)
            session.add(new_item)
        await session.commit()