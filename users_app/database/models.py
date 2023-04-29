from passlib.context import CryptContext
from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    _hashed_password: Mapped[str] = mapped_column(String(512))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean)

    other_name: Mapped[str | None] = mapped_column(String(32), default=None)
    phone: Mapped[str | None] = mapped_column(String(32), default=None)
    birthday: Mapped[str | None] = mapped_column(Date(), default=None)
    city: Mapped[int | None] = mapped_column(ForeignKey('city.id'), default=None)
    additional_info: Mapped[str | None] = mapped_column(String(256), default=None)

    city_relation: Mapped['City'] = relationship(
        back_populates='user_relation',
    )

    @hybrid_property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, password: str):
        self._hashed_password = pwd_context.hash(password)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})'


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)

    user_relation: Mapped['User'] = relationship(
        back_populates='city_relation',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'City(id={self.id!r}, name={self.name!r})'
