import os, asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           WebAppInfo, MenuButtonWebApp)

TOKEN = os.environ["BOT_TOKEN"]
# Render сам подставляет RENDER_EXTERNAL_URL (адрес твоего сервиса)
URL = os.environ.get("WEBAPP_URL") or os.environ["RENDER_EXTERNAL_URL"]

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(m):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=URL))
    ]])
    await m.answer("Добро пожаловать в Aurum Play!\nНажми кнопку, чтобы играть.",
                   reply_markup=kb)


async def index(_):
    return web.FileResponse("index.html")


async def health(_):
    return web.Response(text="ok")


async def main():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000))).start()

    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Играть", web_app=WebAppInfo(url=URL)))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
