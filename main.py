from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from database import init_db, set_nickname, get_nickname
import asyncio
from aiohttp import web

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()

# === РП Нік через /nick ===
@dp.message_handler(commands=["nick"])
async def handle_nick(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Кому ти, блядь, хочеш титул видати? Відповідай на повідомлення адміна.")
        return

    args = message.get_args().strip()
    if not args or "_" not in args:
        await message.reply("Це не нік, а хуйня з під коня. Формат має бути: /nick Імя_Прізвище")
        return

    target_user = message.reply_to_message.from_user
    chat_id = message.chat.id

    try:
        await bot.set_chat_administrator_custom_title(chat_id, target_user.id, args)
        await message.reply(f"Тепер цей єблан має титул: <code>{args}</code>", parse_mode="HTML")
    except Exception as e:
        await message.reply(f"Нічого не вийшло, бо: {e}")

# === Фейковий вебсервер для Render ===
async def handle(request):
    return web.Response(text="I am alive")

def start_health_server():
    app = web.Application()
    app.router.add_get('/', handle)
    web.run_app(app, port=8080)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.to_thread(start_health_server))
    executor.start_polling(dp)
