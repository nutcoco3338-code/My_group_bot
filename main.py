import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- Render အတွက် Web Server သေးသေးလေး ဆောက်ခြင်း ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# --- Telegram Bot Code များ ---
TOKEN = '8837894262:AAGtLVeBrL4DSYxdgqW70W_pajmQzaOhwoc'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('မင်္ဂလာပါ! ကျွန်တော်က Group ထိန်းပေးမယ့် Bot ဖြစ်ပါတယ်။')

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if 'hi' in text:
        await update.message.reply_text('မင်္ဂလာပါ ခင်ဗျာ!')

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text('Kick လုပ်ချင်တဲ့သူရဲ့ စာကို Reply ပြန်ပြီး /kick လို့ ရေးပါ')
        return
    user_id = update.message.reply_to_message.from_user.id
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text('အဖွဲ့ဝင်ကို ထုတ်လိုက်ပါပြီ။')
    except Exception as e:
        await update.message.reply_text(f'Error: {e}')

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text('Mute လုပ်ချင်တဲ့သူရဲ့ စာကို Reply ပြန်ပြီး /mute လို့ ရေးပါ')
        return
    user_id = update.message.reply_to_message.from_user.id
    from telegram import ChatPermissions
    try:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text('အဖွဲ့ဝင်ကို စာရေးခွင့် ပိတ်လိုက်ပါပြီ။')
    except Exception as e:
        await update.message.reply_text(f'Error: {e}')

if __name__ == '__main__':
    # Web Server ကို Thread သီးသန့်ဖြင့် Run ခြင်း
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Bot စတင်ခြင်း
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('kick', kick))
    app.add_handler(CommandHandler('mute', mute))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))
    
    print("Bot is starting...")
    app.run_polling()
    
