from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    hashed_secret_key = Column(String)

    key_keepers = relationship("KeyKeeper", back_populates="user")


class KeyKeeper(Base):
    __tablename__ = 'key_keepers'

    id = Column(Integer, primary_key=True, index=True)
    hashed_name = Column(String)
    hashed_password = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="key_keepers")