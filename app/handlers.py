from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram import Router
from app.weather import get_city, get_weather
import sqlite3

router = Router()
database = sqlite3.connect("db.sqlite3")
cursor = database.cursor()


@router.message(Command("start"))
async def greet(message: Message):
    existence = cursor.execute(f"""
                               SELECT *
                               FROM users
                               WHERE id={message.from_user.id};
                               """).fetchone()
    match existence:
        case None:
            cursor.execute(f"""
                           INSERT INTO users
                           VALUES({message.from_user.id}, 'nowhere');
                           """)
            database.commit()
            await message.answer(
                    text="hi! to set your city type /city [your city]",
                    )
        case _:
            await message.answer(
                    text="you're already registered",
                    )


@router.message(Command("city"))
async def set_city(message: Message, command: CommandObject):
    cursor.execute(f"""
                   UPDATE users
                   SET city='{command.args}'
                   WHERE id={message.from_user.id};
                   """)
    database.commit()
    await message.answer(
            text="success!",
            )


@router.message(Command("forecast"))
async def get_forecast(message: Message):
    city = cursor.execute(f"""
                          SELECT city
                          FROM users
                          WHERE id={message.from_user.id};
                          """).fetchone()[0]
    location = await get_city(city)
    forecast = await get_weather(location)
    await message.answer(
            text=f"""\
todays forecast: {forecast.description}
temperature: {forecast.temp}
it feels like: {forecast.feels_like}
            """
            )
