"""
--создайте алхимичный engine
--добавьте declarative base (свяжите с engine)
--создайте объект Session
--добавьте модели User и Post, объявите поля:
--для модели User обязательными являются name, username, email
--для модели Post обязательными являются user_id, title, body
--создайте связи relationship между моделями: User.posts и Post.user
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Table,
    DateTime,
    func
)

from asyncio import current_task
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declared_attr, InstrumentedAttribute
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

#1 создайте алхимичный engine
PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://user:password@localhost/blog_app"

engine = create_async_engine(
    PG_CONN_URI,
    echo=True,
)

#2 добавьте declarative base (свяжите с engine)
class Base:

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

    def __str__(self):
        attributes = [
            f"{name}={(getattr(self, name))!r}"
            for name, value in vars(self.__class__).items()
            if not name.startswith("_") and isinstance(value, InstrumentedAttribute)
        ]
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def __repr__(self):
        return str(self)


Base = declarative_base(cls=Base, bind=engine)


#3 создайте объект Session
session_factory = sessionmaker(engine)
AsyncSession = async_scoped_session(session_factory, scopefunc=current_task)

#3 Добавьте модели User и Post, объявите поля:
# для модели User обязательными являются name, username, email;
# для модели Post обязательными являются user_id, title, body


class TimestampMixin:
    created_at = Column(DateTime,
                        default=datetime.utcnow,
                        server_default=func.now(),
                        )


#Post
class Post(TimestampMixin, Base):
    __tablename__ = "post"
    user_id = Column(ForeignKey("user.id"))
    title = Column(String(256), nullable=False, default="", server_default="")
    body = Column(Text, nullable=False, default="", server_default="")

    user = relationship("User", back_populates="posts")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, " \
               f"user_id={self.user_id!r}, title={self.title!r}, body={self.body!r})"


#User
class User(TimestampMixin, Base):
    __tablename__ = "user"
    name = Column(String(32), unique=False)
    username = Column(String(32), unique=True)
    email = Column(String, default=False)

    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, " \
               f"name={self.name!r}, username={self.username!r}, email={self.email!r})"