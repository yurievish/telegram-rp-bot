from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from database import init_db, set_nickname, get_nickname

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()

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
