from constants import *
from character import *
from commandHandler import *
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(main_menu)
    
    application.run_polling()

if __name__ == '__main__':
    main()