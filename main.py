import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# --- BotFather ကရတဲ့ TOKEN အမှန်ကို ဒီမှာ ထည့်ပါ ---
TOKEN = '8837894262:AAGtLVeBrL4DSYxdgqW70W_pajmQzaOhwoc'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('မင်္ဂလာပါ! ကျွန်တော်က Group ထိန်းပေးမယ့် Bot ဖြစ်ပါတယ်။')

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()
        if 'hi' in text or 'မင်္ဂလာပါ' in text:
            await update.message.reply_text('မင်္ဂလာပါ ခင်ဗျာ!')
        else:
            await update.message.reply_text(f'သင် ပို့လိုက်သော စာ: {update.message.text}')

if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))
    
    print("Bot is starting...")
    app.run_polling()
    
