import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import yaml

router = Router()

# @router.message(F.text == 'Nigga?')
# async def how(message: Message):
#     await message.answer("Pixff")
#
# @router.message(F.photo)
# async def get_photo(message: Message):
#     await message.answer(f"ID: {message.photo[-1].file_id}")
#

# @router.callback_query(F.data == 'Sosixuy')
# async def messga(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.answer("suk")

def handle_commands(command):
    cmd = command.lstrip("/")

    @router.message(Command(cmd))
    async def handler(message: Message, cmd=cmd):
        buttons = []
        inline_buttons = []

        parse_buttons_for_command(f"/{cmd}", buttons, inline=False)
        parse_buttons_for_command(f"/{cmd}", inline_buttons, inline=True)

        keyboard = [[KeyboardButton(text=i)] for i in buttons]
        main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)

        inline_keyboard = [[
            InlineKeyboardButton(
                text=i["text"],
                url=i["callback_data"] if i["callback_data"].startswith("https") else None,
                callback_data=None if i["callback_data"].startswith("https") else i["callback_data"]
            )
        ] for i in inline_buttons]

        settings = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        if buttons:
            await message.answer(script[f"/{cmd}"]["text"], reply_markup=main)
        elif inline_buttons:
            await message.answer(script[f"/{cmd}"]["text"], reply_markup=settings)
        else:
            await message.answer(script[f"/{cmd}"]["text"])

def handle_text(command):
    @router.message(F.text == command)
    async def handler(message: Message, command=command):
        buttons = []
        inline_buttons = []

        parse_buttons_for_command(f"{command}", buttons, inline=False)
        parse_buttons_for_command(f"{command}", inline_buttons, inline=True)

        keyboard = [[KeyboardButton(text=i)] for i in buttons]
        main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)

        inline_keyboard = [[
            InlineKeyboardButton(
                text=i["text"],
                url=i["callback_data"] if i["callback_data"].startswith("https") else None,
                callback_data=None if i["callback_data"].startswith("https") else i["callback_data"]
            )
        ] for i in inline_buttons]

        settings = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        if buttons:
            await message.answer(script[f"{command}"]["text"], reply_markup=main)
        elif inline_buttons:
            await message.answer(script[f"{command}"]["text"], reply_markup=settings)
        else:
            await message.answer(script[f"{command}"]["text"])

with open('script.txt', 'r', encoding="utf-8") as f:
    script = yaml.safe_load(f)


def parse_buttons_for_command(command, array, inline=False):
    details = script.get(command, {})

    if "buttons" in details:
        for btn, text in details["buttons"].items():
            if not inline:
                array.append(btn)

    if "inline_buttons" in details:
        for btn, text in details["inline_buttons"].items():
            if inline:
                array.append({"text": btn, "callback_data": text})


def check_actions():
    for command, details in script.items():
        if "actions_for_inline" in details:
            for text, callback_data in details["actions_for_inline"].items():
                @router.callback_query(F.data == text)
                async def callback_handler(callback: CallbackQuery, callback_data=callback_data):
                    await callback.answer()
                    await callback.message.answer(callback_data)


def run_f():
    for command in script.keys():
        print(command)
        if command.startswith("/"):
            handle_commands(command)
        else:
            handle_text(command)


async def main():
    check_actions()
    run_f()
    print("Handlers setup completed.")

asyncio.run(main())