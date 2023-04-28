from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import String, Date, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(64))
    is_admin: Mapped[bool] = mapped_column(Boolean)

    other_name: Mapped[Optional[str]] = mapped_column(String(32))
    phone: Mapped[Optional[str]] = mapped_column(String(32))
    birthday: Mapped[Optional[str]] = mapped_column(Date())
    city: Mapped[Optional[int]] = ForeignKey('user.id')
    additional_info: Mapped[Optional[str]] = mapped_column(String(256))

    city_relation: Mapped['City'] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})'


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))

    user: Mapped['User'] = relationship(
        back_populates='city_relation'
    )

    def __repr__(self) -> str:
        return f'City(id={self.id!r}, name={self.name!r})'
