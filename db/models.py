from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class UserPublic(Base):
    __tablename__ = 'user_public'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    public_id = Column(Integer, ForeignKey('public.id'), primary_key=True)
    timestamp = Column(DateTime)
    user = relationship('User', back_populates="publics")
    public = relationship('Public', back_populates="users")


class Public(Base):
    __tablename__ = 'public'
    id = Column(Integer, primary_key=True)
    public_name = Column(String)
    last_post = Column(DateTime)
    last_check = Column(DateTime)
    users = relationship('UserPublic', back_populates='public')

    def __repr__(self):
        return "<Public(public_name='{}', id={})>" \
            .format(self.public_name, self.id)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    publics = relationship('UserPublic', back_populates='user')

    def __repr__(self):
        return "<Users(id={})>" \
            .format(self.id)
