import asyncio
from app.db.session import engine, async_session
from app.models.user import Users
from sqlmodel import select

async def check_users():
    async with async_session() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        print("=== Окно юзера ===")
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Role: {user.role}")
            print(f"Teacher ID: {user.teacher_id}")
            print("---")

if __name__ == "__main__":
    asyncio.run(check_users())