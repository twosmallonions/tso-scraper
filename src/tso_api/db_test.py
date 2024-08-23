from typing import Optional
from sqlalchemy import ForeignKey, create_engine, select, text, String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine(
    'postgresql+psycopg://postgres:postgres@localhost:5432/postgres', echo=True
)

with Session(engine) as conn:
    conn.execute(text('CREATE TABLE some_table (x int, y int)'))
    result = conn.execute(text('SELECT x, y FROM some_table WHERE y > :y'), {'y': 2})
    for row in result:
        print(row)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[list['Address']] = relationship(back_populates='user')
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey('user_account.id'))

    user: Mapped[User] = relationship(back_populates='addresses')

    def __repr__(self) -> str:
        return f'Address(id={self.id!r}, email_address={self.email_address!r})'

Base.metadata.create_all(engine)
sandy = User(name='sandy', fullname='Ass Cheeks')
me = User(name='marius', fullname='Marius Meschter')
print(sandy)
session = Session(engine)
session.add(sandy)
session.add(me)
session.flush()
db_sandy = session.get(User, sandy.id)
print(db_sandy)
print(db_sandy is sandy)
session.commit()
me.name = 'actually not me'
print('===============================')
print(session.dirty)
me_fullname = session.execute(select(User.fullname).where(User.id == me.id)).scalar_one()
print(me_fullname)
session.close()