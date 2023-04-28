from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(64))
    is_admin: Mapped[bool] = mapped_column(Boolean)

    other_name: Mapped[str | None] = mapped_column(String(32))
    phone: Mapped[str | None] = mapped_column(String(32))
    birthday: Mapped[str | None] = mapped_column(Date())
    city: Mapped[int | None] = ForeignKey('user.id')
    additional_info: Mapped[str | None] = mapped_column(String(256))

    city_relation: Mapped['City'] = relationship(
        back_populates='user_relation', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})'


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))

    user_relation: Mapped['User'] = relationship(
        back_populates='city_relation'
    )

    def __repr__(self) -> str:
        return f'City(id={self.id!r}, name={self.name!r})'
