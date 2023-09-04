import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from config import TOKEN

# All handlers should be attached to the Router (or Dispatcher)
# Initializes a dispatcher instance
dp = Dispatcher()


@dp.message(Command('custom'))
async def command_help_handler(message: Message) -> None:
    """ `/custom` command handler """

    await message.answer(f"come up with the /custom command logic on your own!")


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    """ `/help` command handler """

    await message.answer(f"this is the /help command reaction!")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """ `/start` command handler"""

    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler forwards a received message back to the sender

    It handles the majority (like a text, photo, sticker etc.)
    but not all the message types
    """
    try:
        # Sends back a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # starts running events polling and dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())