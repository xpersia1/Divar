import pandas as pd
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import re

TOKEN = ("8152891768:AAE1zL57parZHZwH0J7djv-e38HliNjaJgk")
PASSWORD = "secret123"  # پسورد موردنظر

df = pd.read_csv('../data/raw/best_value_houses.csv')
authorized_users = set()  # لیست کاربران تأیید شده

def clean_text(text):
    return re.sub(r'[*_`]', '', text)

async def check_password(update, context):
    chat_id = update.message.chat_id
    user_input = update.message.text.strip()

    if user_input == PASSWORD:
        authorized_users.add(chat_id)
        await update.message.reply_text("✅ رمز عبور صحیح است! حالا می‌توانی /start را بفرستی.")
    else:
        await update.message.reply_text("❌ رمز عبور اشتباه است! دوباره امتحان کن.")

async def send_ads(update, context):
    chat_id = update.message.chat_id

    if chat_id not in authorized_users:
        await update.message.reply_text("🚫 لطفاً ابتدا رمز عبور را وارد کنید.")
        return

    for _, row in df.iterrows():
        text = f"""
        🏠 <b>{row['عنوان']}</b>
        📍 <b>محله:</b> {row['محله']}
        💰 <b>قیمت:</b> {row['قیمت']:,.0f} تومان
        🔗 <a href="{row['لینک']}">لینک آگهی</a>
        """
        await context.bot.send_message(chat_id=chat_id, text=clean_text(text), parse_mode='HTML')

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))
app.add_handler(CommandHandler("start", send_ads))
app.run_polling(drop_pending_updates=True)

print("✅ ربات محافظت‌شده با رمز عبور راه‌اندازی شد!")
