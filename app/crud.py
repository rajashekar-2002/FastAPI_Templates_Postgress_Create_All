from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Item

# CREATE item
async def create_item(db: AsyncSession, name: str):
    # Create Python object
    item = Item(name=name)

    # Add to DB session
    db.add(item)

    # 🔹 await commit
    # WHY await?
    # - DB write is slow
    # - Let server do other work meanwhile
    await db.commit()

    # Refresh object to get ID from DB
    await db.refresh(item)

    return item

# READ items
async def get_items(db: AsyncSession):
    # 🔹 await execute
    # WHY?
    # - SQL query is I/O
    result = await db.execute(select(Item))

    # Convert result to list
    return result.scalars().all()

# DELETE item
async def delete_item(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(Item).where(Item.id == item_id)
    )

    item = result.scalar_one_or_none()

    if item:
        await db.delete(item)
        await db.commit()
