from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from config import MQTT_PARAMETERS
from controller import publish, get_status

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="/help")],
        [types.KeyboardButton(text="/status")]
    ])

    await msg.answer("Данный бот представляет из себя интерфейс для системы управления виртуальным устройством. Для "
                     "получения информации о командах введите \"/help\"", reply_markup=keyboard)


@router.message(Command("help"))
async def message_handler(msg: Message):
    await msg.answer(f"""Поддерживаемые команды:
        1. /help - информация обо всех командах
        2. /status - информация обо всех устройствах системы
        3. /state "параметр" "состояние" - изменить состояние параметра устройства. Параметры текущего устройства - \
        {", ".join(MQTT_PARAMETERS)} 
    """)


@router.message(Command("status"))
async def message_handler(msg: Message):
    await msg.answer(
        "Состояние текущего устройства:\n" + get_status()
    )


@router.message(Command("state"))
async def message_handler(msg: Message, command: CommandObject):
    parameter, state = command.args.split()

    if parameter not in MQTT_PARAMETERS:
        await msg.answer(
            f'Некорректный параметр. Параметр должен находиться в списке: {", ".join(MQTT_PARAMETERS)}'
        )
        return

    answer = publish(parameter, state)

    await msg.answer(
        "Опубликовано: " + answer
    )
