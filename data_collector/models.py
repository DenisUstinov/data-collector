from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pair = Column(String(10), index=True, nullable=False)
    trade_id = Column(Integer, unique=True, nullable=False)
    type = Column(String(4), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    amount = Column(Float)
    ts = Column(BigInteger, index=True, nullable=False)

class Ticker(Base):
    __tablename__ = 'tickers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pair = Column(String(10), index=True, nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    last_trade = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    avg = Column(Float, nullable=False)
    vol = Column(Float, nullable=False)
    vol_curr = Column(Float, nullable=False)
    ts = Column(BigInteger, index=True, nullable=False)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pair = Column(String(10), index=True, nullable=False)
    ask_price = Column(Float, nullable=False)
    ask_quantity = Column(Float, nullable=False)
    ask_amount = Column(Float, nullable=False)
    bid_price = Column(Float, nullable=False)
    bid_quantity = Column(Float, nullable=False)
    bid_amount = Column(Float, nullable=False)
    ts = Column(BigInteger, index=True, nullable=False)