import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("7532994082:AAHVLyzK9coVgvCp-nwXL1MfPS0X57yZAmk")
API_URL = "https://vehicle-details-api.vercel.app/details/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚗 Welcome to Vehicle Info Bot!\nUse /check <VEHICLE_NO>\nExample: /check MH12AB1234")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Please provide a vehicle number.\nUsage: /check MH12AB1234")
        return

    vehicle_no = context.args[0].upper()
    try:
        res = requests.get(API_URL + vehicle_no)
        data = res.json()

        if data.get("error"):
            await update.message.reply_text(f"❌ Error: {data['error']}")
            return

        msg = f"🚘 *Vehicle Details for {vehicle_no}*:\n"
        msg += f"• Owner: {data.get('owner_name', 'N/A')}\n"
        msg += f"• Registration Date: {data.get('registration_date', 'N/A')}\n"
        msg += f"• Manufacturer: {data.get('maker_description', 'N/A')}\n"
        msg += f"• Model: {data.get('model', 'N/A')}\n"
        msg += f"• Fuel Type: {data.get('fuel_type', 'N/A')}\n"
        msg += f"• Vehicle Class: {data.get('vehicle_class', 'N/A')}\n"
        msg += f"• RC Status: {data.get('rc_status', 'N/A')}\n"
        msg += f"• Insurance: {data.get('insurance_upto', 'N/A')}\n"

        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Failed to fetch details. Try again later.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling()

if __name__ == "__main__":
    main()
