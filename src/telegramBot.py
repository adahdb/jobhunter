import json
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import services

async def send_jobs(jobs):
    bot = services.telegram_app.bot


    message = f"🗂 Today's Job Listings [{len(jobs)} Jobs]:\n\n"
    for job in jobs:
        job_message = f"📌 {job['headline']}\n"
        job_message += f"🏢 {job['employer']}\n"
        job_message += f"📂 {job['occupation_group_label']}\n"
        job_message += f"📅 {job['timePosted']}\n"
        job_urls = json.loads(job['urls'])
        for url in job_urls:
            job_message += f"🔗 {url}\n"
        job_message += "─────────────────\n"

        if len(message) + len(job_message) > 4000:
            await bot.send_message (chat_id=TELEGRAM_CHAT_ID, text=message)
            message = job_message
        else:
            message += job_message

    if message: 
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")
    print(update.message.chat.id)

async def init():
    services.telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    services.telegram_app.add_handler(CommandHandler("start", start))

    await services.telegram_app.initialize()
    await services.telegram_app.start()
    await services.telegram_app.updater.start_polling()

