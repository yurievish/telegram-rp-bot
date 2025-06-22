from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from database import init_db
import asyncio
from aiohttp import web

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()

# === Команда /nick для видачі титулу ===
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
        # Піднімаємо юзера до адміна (навіть якщо він вже адмін — так стабільніше)
        await bot.promote_chat_member(
            chat_id=chat_id,
            user_id=target_user.id,
            can_manage_chat=False,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False
        )

        # Ставимо титул
        await bot.set_chat_administrator_custom_title(chat_id, target_user.id, args)
        await message.reply(f"Тепер цей єблан має титул: <code>{args}</code>", parse_mode="HTML")

    except Exception as e:
        await message.reply(f"Нічого не вийшло, бо: {e}")

# === Фейковий health-check сервер для Render ===
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
