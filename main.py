from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token အသစ် ထည့်သွင်းထားပြီးဖြစ်ပါသည်
TOKEN = '8837894262:AAGtLVeBrL4DSYxdgqW70W_pajmQzaOhwoc'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ Bot မှ ကြိုဆိုပါတယ်ခင်ဗျာ။")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if 'hi' in text or 'hello' in text:
        await update.message.reply_text("Hi! မင်္ဂလာပါဗျာ၊ ဘာကူညီပေးရမလဲ။")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_status = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if user_status.status not in ['administrator', 'creator']:
        await update.message.reply_text("ဒီ Command ကို Admin တိုင်ပဲ သုံးလို့ရပါတယ်။")
        return
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, target_user.id)
        await update.message.reply_text(f"User {target_user.mention_html()} ကို Group ထဲမှ ထုတ်လိုက်ပါပြီ။", parse_mode='HTML')

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_status = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if user_status.status not in ['administrator', 'creator']:
        await update.message.reply_text("ဒီ Command ကို Admin တိုင်ပဲ သုံးလို့ရပါတယ်။")
        return
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        from telegram import ChatPermissions
        await context.bot.restrict_chat_member(
            update.effective_chat.id, 
            target_user.id, 
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(f"User {target_user.mention_html()} ကို Mute လုပ်လိုက်ပါပြီ။", parse_mode='HTML')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("kick", kick_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    print("Bot စတင်ပွင့်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
      
