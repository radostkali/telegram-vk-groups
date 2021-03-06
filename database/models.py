from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class LastRefresh(Base):
    __tablename__ = 'last_refresh'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)


class UserPublic(Base):
    __tablename__ = 'user_public'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    public_id = Column(Integer, ForeignKey('public.id'), primary_key=True)
    user = relationship('User', back_populates="publics")
    public = relationship('Public', back_populates="users")


class Public(Base):
    __tablename__ = 'public'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug_url = Column(String)

    users = relationship('UserPublic', back_populates='public')

    def __repr__(self):
        return "<Public(name='{}', id={})>".format(self.name, self.id)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    publics = relationship('UserPublic', back_populates='user')

    def __repr__(self):
        return "<Users(id={})>".format(self.id)

