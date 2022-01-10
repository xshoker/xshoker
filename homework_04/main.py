import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Base, engine, User, Post
from jsonplaceholder_requests import USERS_DATA_URL, POSTS_DATA_URL
from aiohttp import ClientSession

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def create_tables():
    """
    If we aren't using alembic
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def fetch_user():
    async with ClientSession() as session:
        async with session.get(USERS_DATA_URL) as response:
            return await response.json()


async def fetch_posts():
    async with ClientSession() as session:
        async with session.get(POSTS_DATA_URL) as response:
            return await response.json()


async def async_main():
    await create_tables()
    users, posts = await asyncio.gather(
        fetch_user(),
        fetch_posts(),
    )
    async with async_session() as session:
        async with session.begin():
            for user in users:
                session.add(User(id=user['id'], name=user['name'], username=user['username'], email=user['email']))
            for post in posts:
                session.add(Post(id=post['id'], user_id=post['userId'], title=post['title'], body=post['body']))


def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(async_main())

if __name__ == '__main__':
    main()