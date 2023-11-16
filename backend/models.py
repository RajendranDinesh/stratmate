from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

# Define SQLAlchemy models
Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, ForeignKey("players.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    progress = Column(Integer, nullable=False)

class RatingHistory(Base):
    __tablename__ = "rating_history"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, ForeignKey("players.id"), nullable=False)
    day_1 = Column(Integer)
    day_2 = Column(Integer)
    day_3 = Column(Integer)
    day_4 = Column(Integer)
    day_5 = Column(Integer)
    day_6 = Column(Integer)
    day_7 = Column(Integer)
    day_8 = Column(Integer)
    day_9 = Column(Integer)
    day_10 = Column(Integer)
    day_11 = Column(Integer)
    day_12 = Column(Integer)
    day_13 = Column(Integer)
    day_14 = Column(Integer)
    day_15 = Column(Integer)
    day_16 = Column(Integer)
    day_17 = Column(Integer)
    day_18 = Column(Integer)
    day_19 = Column(Integer)
    day_20 = Column(Integer)
    day_21 = Column(Integer)
    day_22 = Column(Integer)
    day_23 = Column(Integer)
    day_24 = Column(Integer)
    day_25 = Column(Integer)
    day_26 = Column(Integer)
    day_27 = Column(Integer)
    day_28 = Column(Integer)
    day_29 = Column(Integer)
    day_30 = Column(Integer)

class UserRegister(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)