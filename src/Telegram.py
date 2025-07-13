import pandas as pd
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import re

# ⚙️ مشخصات ثابت
TOKEN = "8152891768:AAE1zL57parZHZwH0J7djv-e38HliNjaJgk"
PASSWORD = "secret123"
DATA_FOLDER = "/Users/x/Divar/src/data/analysis"

AUTHORIZED_USERS = set()

# 🧹 پاکسازی متن
def clean_text(text):
    return re.sub(r'[*_`]', '', text)

# ✅ مدیریت رمز عبور
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip()

    if user_input == PASSWORD:
        AUTHORIZED_USERS.add(chat_id)
        await update.message.reply_text("✅ رمز عبور درست بود! برای شروع دستور /help رو بفرست.")
    else:
        await update.message.reply_text("❌ رمز اشتباهه! دوباره تلاش کن.")

# ✅ راهنما
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in AUTHORIZED_USERS:
        await update.message.reply_text("🚫 لطفاً ابتدا رمز عبور رو بفرست.")
        return

    help_text = (
        "🤖 <b>دستورات ربات:</b>\n\n"
        "/desc - آمار توصیفی\n"
        "/avg - میانگین قیمت هر متر در محله‌ها\n"
        "/best - لیست بهترین خانه‌ها برای خرید\n"
        "/plots - مشاهده نمودارها\n"
    )
    await update.message.reply_text(help_text, parse_mode='HTML')

# ✅ آمار توصیفی
async def send_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in AUTHORIZED_USERS:
        await update.message.reply_text("🚫 لطفاً ابتدا رمز عبور رو بفرست.")
        return

    desc_file = os.path.join(DATA_FOLDER, "descriptive_stats.csv")
    await context.bot.send_document(chat_id=chat_id, document=open(desc_file, "rb"))
    await update.message.reply_text("✅ آمار توصیفی داده‌ها ارسال شد.")

# ✅ میانگین قیمت هر متر
async def send_avg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in AUTHORIZED_USERS:
        await update.message.reply_text("🚫 لطفاً ابتدا رمز عبور رو بفرست.")
        return

    avg_file = os.path.join(DATA_FOLDER, "region_avg_price.csv")
    plot_file = os.path.join(DATA_FOLDER, "region_avg_price_plot.png")

    await context.bot.send_document(chat_id=chat_id, document=open(avg_file, "rb"))
    await context.bot.send_photo(chat_id=chat_id, photo=open(plot_file, "rb"))
    await update.message.reply_text("✅ میانگین قیمت هر متر و نمودارش ارسال شد.")

# ✅ بهترین خانه‌ها
async def send_best(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in AUTHORIZED_USERS:
        await update.message.reply_text("🚫 لطفاً ابتدا رمز عبور رو بفرست.")
        return

    best_file = os.path.join(DATA_FOLDER, "best_value_houses.csv")
    df_best = pd.read_csv(best_file)

    for _, row in df_best.iterrows():
        text = f"""
🏠 <b>{row['عنوان']}</b>
📍 <b>محله:</b> {row['محله']}
💰 <b>قیمت:</b> {row['قیمت']:,.0f} تومان
📐 <b>متراژ:</b> {row['متراژ']} متر
🛏️ <b>اتاق:</b> {row['تعداد اتاق']}
💸 <b>قیمت هر متر:</b> {row['قیمت هر متر']:,.0f} تومان
🔗 <a href="{row['لینک']}">لینک آگهی</a>
        """
        await context.bot.send_message(chat_id=chat_id, text=clean_text(text), parse_mode='HTML')

    await update.message.reply_text("✅ لیست 20 خانه با بهترین ارزش خرید ارسال شد.")

# ✅ ارسال تمام نمودارها
async def send_plots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in AUTHORIZED_USERS:
        await update.message.reply_text("🚫 لطفاً ابتدا رمز عبور رو بفرست.")
        return

    plots = [
        "region_avg_price_plot.png",
        "price_distribution_plot.png",
        "price_vs_area_plot.png",
        "rooms_distribution_plot.png",
    ]

    for plot_name in plots:
        path = os.path.join(DATA_FOLDER, plot_name)
        await context.bot.send_photo(chat_id=chat_id, photo=open(path, "rb"))

    await update.message.reply_text("✅ همه نمودارها ارسال شد.")

# ------------------------------------------------
# ⚡️ ساخت و راه‌اندازی بات
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("desc", send_desc))
app.add_handler(CommandHandler("avg", send_avg))
app.add_handler(CommandHandler("best", send_best))
app.add_handler(CommandHandler("plots", send_plots))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

print("✅ ربات محافظت‌شده با رمز عبور راه‌اندازی شد!")
app.run_polling(drop_pending_updates=True)
