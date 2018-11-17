import time
import telegram
from telegram.ext import *
from telegram import *
from config import teletoken

# set up button layout
keyboard = [[InlineKeyboardButton('up', callback_data='U')],
            [InlineKeyboardButton('left', callback_data='L'), InlineKeyboardButton('right', callback_data='R')],
            [InlineKeyboardButton('down', callback_data='D')]]
 
reply_markup = InlineKeyboardMarkup(keyboard)

display = ""
reading = False
writing = False

def start(bot, update):
    global display
    global reading
    if not reading:
        reading = True
        f = open('Server.txt', 'r', encoding='utf-8')
        display = f.read()
        bot.send_message(chat_id=update.message.chat_id, text=display, reply_markup=reply_markup)
        print('sent')
        f.close()
        reading = False

def buttons(bot, update):
    global display
    global reading
    global writing
    if not writing:
        writing = True
        f = open('Client.txt', 'w')
        f.write(update.callback_query.data + '\n')
        f.close()
        writing = False
    time.sleep(.5)
    if not reading:
        reading = True
        f = open('Server.txt', 'r', encoding='utf-8')
        display = f.read()
        print('read')
        bot.edit_message_text(chat_id=update.callback_query.message.chat.id,
                        message_id=update.callback_query.message.message_id,
                        text=display,
                        reply_markup=reply_markup)
        f.close()
        reading = False
    

def main():
    # setup
    updater = Updater(token=teletoken)   # don't hax0r me
    dispatcher = updater.dispatcher

    # setup event handlers
    start_handler = CommandHandler('start', start)
    buttons_handler = CallbackQueryHandler(buttons)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(buttons_handler)

    # start
    updater.start_polling()
    
    # enable ctrl+c termination
    updater.idle()

if __name__ == '__main__':
    main()