import logging
from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes
from telegram.constants import ChatMemberStatus

BOT_TOKEN = "8868530843:AAFyH6CZBPVxk0tOFaj9mer2LZLoFi-ZH3w"
ADMIN_CHAT_ID = 749890854

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def track_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if not result:
        return

    old_status = result.old_chat_member.status
    new_status = result.new_chat_member.status
    user = result.new_chat_member.user
    chat = result.chat

    name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else "нет username"
    profile_link = f"tg://user?id={user.id}"
    date = result.date.strftime("%d.%m.%Y %H:%M:%S")

    JOINED = {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER}
    LEFT = {ChatMemberStatus.LEFT, ChatMemberStatus.BANNED}

    was_member = old_status in JOINED
    is_member = new_status in JOINED

    if not was_member and is_member:
        action = "✅ ПОДПИСАЛСЯ"
    elif was_member and not is_member:
        action = "❌ ОТПИСАЛСЯ"
    else:
        return

    message = (
        f"{action}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📢 Канал: {chat.title}\n"
        f"👤 Имя: {name}\n"
        f"🔗 Ник: {username}\n"
        f"🆔 ID: {user.id}\n"
        f"🔑 Профиль: {profile_link}\n"
        f"🕐 Дата/время: {date}"
    )

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)


async def post_init(app):
    await app.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text="🤖 Бот запущен и отслеживает подписки/отписки в твоих каналах!"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(ChatMemberHandler(track_member, ChatMemberHandler.CHAT_MEMBER))
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=["chat_member"])


if __name__ == "__main__":
    main()
