import asyncio
import aiohttp
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import dotenv_values

# Initializes a dispatcher instance. All handlers should be attached to the Router (or Dispatcher).
dp = Dispatcher()

# Creates a dictionary of env vars out of .env file content.
config = dotenv_values('.env')


@dp.message(Command('weather'))
async def command_weather_handler(message: Message) -> None:
    """
    '/weather' command handler. Parses the command, requests weather info from https://api.openweathermap.org.
    There are latitude and longitude values of Karaganda, KZ hardcoded in the request plus openweathermap.org API token.

    :param message: Text message from Telegram API.
    :return: None
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://api.openweathermap.org/data/2.5/weather?'
                    f'lat=49.8161282&lon=73.1026622&appid={config["OPEN_WEATHER_TOKEN"]}&units=metric') as response:
                data = await response.json()
                date_time = datetime.datetime.now()
                await message.answer(f"Weather conditions in {data['name']}\n\n"
                                     f"date: {date_time.day}_{date_time.month}_{date_time.year}\n"
                                     f"time: {date_time.hour}:{date_time.minute}\n"
                                     f"temperature: {data['main']['temp']} \u00B0C\n"
                                     f"humidity: {data['main']['humidity']} %\n"
                                     f"wind speed: {data['wind']['speed']} m/s\n\n"
                                     f"feels like: {data['main']['feels_like']} \u00B0C\n"
                                     f"text description: {data['weather'][0]['description']}")

    except Exception as ex:
        print(ex)


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    """
    '/help' command handler. It parses the command and reacts with a text message.

    :param message: Text message from Telegram API.
    :return: None
    """

    await message.answer(f"this is the /help command reaction!")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    '/start' command handler. It parses the command and reacts with a text message.

    :param message: Text message from Telegram API.
    :return: None
    """

    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    The handler forwards a received message back to the sender.

    It handles the majority (like a text, photo, sticker etc.) but not all the message types.

    :param message: Text message from Telegram API.
    :return: None
    """

    try:
        # Sends back a copy of the received message.
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it.
        await message.answer("Nice try!")


async def main() -> None:
    """
    Main func. Initialize Bot instance with a default parse mode which will be passed to all API calls.

    :return: None
    """

    bot = Bot(config['TELEGRAM_TOKEN'], parse_mode=ParseMode.HTML)

    # Starts running events polling and dispatching.
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Launches the asyncio event loop.
    asyncio.run(main())
