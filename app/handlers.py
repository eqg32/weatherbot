from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram import Router

router = Router()


@router.message(Command("start"))
async def greet(message: Message):
    pass


@router.message(Command("city"))
async def set_city(message: Message, command: CommandObject):
    pass


@router.message(Command("weater"))
async def get_forecast(message: Message):
    pass
