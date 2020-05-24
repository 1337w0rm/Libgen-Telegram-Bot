#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BookInfo import BookInfoProvider
from common import TELEGRAM_ACCESS_TOKEN, logging, logger, mode, HEROKU_APP_NAME
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os, sys, wget, glob
from functools import wraps
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


# Create the EventHandler and pass it your bot's token.
updater = Updater(token = TELEGRAM_ACCESS_TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TELEGRAM_ACCESS_TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TELEGRAM_ACCESS_TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

def button(update, context):
    query = update.callback_query
    query_data = int(query.data)
    print(query_data)
    provider = BookInfoProvider()
    books = provider.load_book_list(text, 'title')


    dl = books[query_data].download_links[0]
    if not os.path.exists('book'):
      os.makedirs('book')
    wget.download(dl,'book/')

    os.chdir('book')
    for file in glob.glob("*." + str(books[query_data].format)):
        filename = file

    context.bot.send_document(chat_id=update.effective_message.chat_id, document=open(filename, 'rb'),timeout = 120)
    os.remove(filename)
    for m in mid:
        context.bot.delete_message(chat_id=update.effective_message.chat_id, message_id=m.message_id)



def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator


send_typing_action = send_action(ChatAction.TYPING)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update,context):
    """Send a message when the command /start is issued."""
    print('Start')
    update.message.reply_text('Hi! Type your book title, I will try to find it.')


def help(update,context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


@send_typing_action
def echo(update,context):
	try:
		pass
		provider = BookInfoProvider()
		books = provider.load_book_list(update.message.text, 'title')
		global text
		global mid
		text = update.message.text 
		mid = list()
		keyboard = list()
		ids = list()
		for book in books:
			mid.append(update.message.reply_text(str(book)))
			ids.append(book.id)
		if len(ids) != 0:    
			for each,i in zip(ids,range(len(ids))):
				keyboard.append(InlineKeyboardButton(each, callback_data = i))
				reply_markup=InlineKeyboardMarkup(build_menu(keyboard,n_cols=5)) 
			mid.append(context.bot.send_message(chat_id=update.message.chat_id, text='Choose Book ID',reply_markup=reply_markup))
		else:
			update.message.reply_text("Sorry, Book not found! :'(")
	except:
		update.message.reply_text("Some Weird Error Occured! RETRY.")

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_handler(CallbackQueryHandler(button))

    run(updater)

if __name__ == '__main__':
    main()