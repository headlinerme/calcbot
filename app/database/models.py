import os
from dotenv import load_dotenv

from sqlalchemy import ForeignKey, BigInteger, String, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


load_dotenv()
engine = create_async_engine(os.getenv("DB_URL"), echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    userID = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    queryCount: Mapped[int] = mapped_column()
    queryUsedCount: Mapped[int] = mapped_column()
    tokensUsedCount: Mapped[int] = mapped_column()
    warns: Mapped[int] = mapped_column()


class UserData(Base):
    __tablename__ = "usersData"

    userDataID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))
    gender: Mapped[str] = mapped_column(String(7))
    age: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()
    lifestyle: Mapped[str] = mapped_column(String(255))
    goal: Mapped[str] = mapped_column(String(255))
    standard = mapped_column(JSON)


class DailyReport(Base):
    __tablename__ = "dailyReports"

    dailyReportID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))
    calculationDate: Mapped[str] = mapped_column()
    mealDescription: Mapped[str] = mapped_column()
    dailyReport = mapped_column(JSON)
    dailyWarns: Mapped[int] = mapped_column()
    
    
# class Dairy(Base):
#     __tablename__ = "diaries"
    
#     dairyID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))


async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
