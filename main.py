from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from database import init_db
import asyncio
from aiohttp import web

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()

@dp.message_handler(commands=["nick"])
async def handle_nick(message: types.Message):
    if not message.reply_to_message:
        await message.reply("⚠️ Ви не відповіли на повідомлення!
Щоб призначити титул, скористайтесь командою у відповіді на повідомлення користувача.")
        return

    args = message.get_args().strip()
    if not args or "_" not in args:
        await message.reply("❗ Некоректний формат!
Будь ласка, використовуйте формат: <code>/nick Ім'я_Прізвище</code>", parse_mode="HTML")
        return

    target_user = message.reply_to_message.from_user
    chat_id = message.chat.id

    try:
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

        await asyncio.sleep(1.5)

        await bot.set_chat_administrator_custom_title(chat_id, target_user.id, args)
        await message.reply(f"✅ Успіх!
Користувачу <b>{target_user.full_name}</b> призначено титул: <code>{args}</code>", parse_mode="HTML")

    except Exception as e:
        if "USER_NOT_ADMIN" in str(e) or "not an administrator" in str(e):
            await message.reply("🛑 Неможливо призначити титул!
Telegram дозволяє це лише адміністраторам.
Перевірте, чи користувач має статус адміністратора.")
        elif "CHAT_ADMIN_REQUIRED" in str(e) or "rights" in str(e):
            await message.reply("🔒 Обмеження!
Бот не має достатніх прав для зміни титулу користувача.
Перевірте налаштування прав адміністратора для бота.")
        else:
            await message.reply(f"❌ Виникла помилка:
<code>{e}</code>", parse_mode="HTML")

# Health-check сервер для Render
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
