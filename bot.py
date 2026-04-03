from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from db import get_doc, collection, get_all_docs
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
async def handle_message(update : Update, context : ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    if update.message.document:
        file_id = update.message.document.file_id
        context.user_data["pending_file"] = file_id
        await update.message.reply_text("Enter a name for this file: ")
        return
    if "pending_file" in context.user_data:
        file_id = context.user_data["pending_file"]
        name = update.message.text.lower()
        collection.insert_one({
            "keyword" : name,
            "file_path" : file_id
        })   
        context.user_data.pop("pending_file")
        await update.message.reply_text("File uploaded successfully")
    text = update.message.text.lower()
    doc = get_doc(text)
    if doc:
        await update.message.reply_document(
            document = doc["file_path"],
            caption = doc["keyword"]
        )
    else:
        await update.message.reply_text("Document not found")
async def start(update, context):
    docs = get_all_docs()
    if not docs:
        await update.message.reply_text("No documents available yet")
        return
    message = "Available Documents: \n\n"
    for doc in docs:
        message += f" {doc['keyword']}\n"
    message += "\n Send the name to get the file"
    await update.message.reply_text(message)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        (filters.TEXT & ~filters.COMMAND )| filters.Document.ALL,
        handle_message 
    )
)
app.run_polling() 
