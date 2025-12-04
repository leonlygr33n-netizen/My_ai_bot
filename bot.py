import os
import logging
from rembg import remove
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me any photo and I will remove the background for you!"
    )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    input_path = "input.jpg"
    output_path = "output.png"

    await file.download_to_drive(input_path)

    try:
        with open(input_path, "rb") as i:
            with open(output_path, "wb") as o:
                o.write(remove(i.read()))

        await update.message.reply_photo(photo=open(output_path, "rb"))
    except:
        await update.message.reply_text("❌ Something went wrong. Try again.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
