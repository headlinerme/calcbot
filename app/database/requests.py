from app.database.models import async_session
from app.database.models import User, UserData, DailyReport
from sqlalchemy import select, update, delete


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return inner


@connection
async def set_user(session, userID: int) -> None:
    result = await session.execute(
        select(User)
        .where(User.userID == userID)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        session.add(
            User(
                userID=userID,
                queryCount=0,
                queryUsedCount=0,
                tokensUsedCount=0,
                warns=0,
            )
        )
        await session.commit()


@connection
async def set_user_data(
    session,
    userID: int,
    gender: str,
    age: int,
    height: int,
    weight: int,
    lifestyle: str,
    goal: str,
    standard: dict,
) -> None:
    result = await session.execute(
        select(UserData)
        .where(UserData.userID == userID)
    )
    user_data = result.scalar_one_or_none()
    
    if not user_data:
        session.add(
            UserData(
                userID=userID,
                gender=gender,
                age=age,
                height=height,
                weight=weight,
                lifestyle=lifestyle,
                goal=goal,
                standard=standard,
            )
        )
        await session.commit()


@connection
async def get_user_data(session, userID: int):
    return await session.scalars(
        select(UserData)
        .where(UserData.userID == userID)
    )


@connection
async def update_user_data(
    session,
    userID: int,
    gender: str,
    age: int,
    height: int,
    weight: int,
    lifestyle: str,
    goal: str,
    standard: dict,
) -> None:
    await session.execute(
        update(UserData)
        .where(UserData.userID == userID)
        .values(
            userID=userID,
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            lifestyle=lifestyle,
            goal=goal,
            standard=standard,
        )
    )
    await session.commit()


@connection
async def user_send_request(
    session,
    userID: int,
    queryCount: int,
    queryUsedCount: int,
    tokensUsedCount: int,
    warns: int,
) -> None:
    await session.execute(
        update(User)
        .where(User.userID == userID)
        .values(
            userID=userID,
            queryCount=User.queryCount - queryCount,
            queryUsedCount=User.queryUsedCount + queryUsedCount,
            tokensUsedCount=User.tokensUsedCount + tokensUsedCount,
            warns=User.warns + warns,
        )
    )
    await session.commit()


@connection
async def set_daily_report(
    session,
    userID: int,
    calculationDate: str,
    mealDescription: str,
    dailyReport: dict,
    dailyWarns: int,
) -> None:
    session.add(
        DailyReport(
            userID=userID,
            calculationDate=calculationDate,
            mealDescription=mealDescription,
            dailyReport=dailyReport,
            dailyWarns=dailyWarns,
        )
    )
    await session.commit()


@connection
async def get_daily_report(session, userID: int, calculationDate: str):
    return await session.scalars(
        select(DailyReport)
        .where(
            (DailyReport.userID == userID) 
            & (DailyReport.calculationDate.startswith(calculationDate))
        )
    )


@connection
async def delete_daily_report(session, userID: int, mealDescription: str) -> None:
    await session.execute(
        delete(DailyReport)
        .where(
            (DailyReport.userID == userID)
            & (DailyReport.mealDescription == mealDescription)
        )
    )
    await session.commit()
