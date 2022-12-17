from fileinput import filename
import logging
import os

from telegram import *
from telegram.ext import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CLICK_BUTTON,GET_NAME, RECV_IMAGE_NAME, RECV_IMAGE_FILE, DELETE_FILE = range(5)
# Define a few command handlers. These usually take the two arguments update and
# context.

def cancel(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    
    context.user_data.clear()
    update.message.reply_text("Cancel!")
    return ConversationHandler.END

def start_create(update: Update, context: CallbackContext):
    update.message.reply_text("Enter image name")
    return RECV_IMAGE_NAME

def recv_name(update: Update, context: CallbackContext):
    context.user_data['filename'] = update.message.text
    update.message.reply_text(f"You have entered {context.user_data['filename']}")
    return RECV_IMAGE_FILE

def recv_image(update: Update, context: CallbackContext):
    file_id = update.message.photo[-1].file_id
    file = context.bot.getFile(file_id)
    file.download(f"{context.user_data['filename']}"+ ".jpg")
    
    text = "Upload success\n\n-> If you want to check a upload work?\n-> click the /read !!"
    context.bot .send_message(update.effective_user.id, text =text)

    return ConversationHandler.END

def read(update: Update, context: CallbackContext) -> int:
    ###
    # DB 혹은 csv형태로 저장된 key와 파일경로 
    ###

    show_list =[]

    file_names = os.listdir()
    for filename in file_names:
        if os.path.splitext(filename)[1] == '.jpg':
            show_list += [[InlineKeyboardButton(filename.rsplit('.')[0], callback_data = filename.rsplit('.')[0])]]

    show_markup = InlineKeyboardMarkup(show_list)

    update.message.reply_text("Click Button",reply_markup=show_markup)
    
    return CLICK_BUTTON


def read_button(update: Update, context: CallbackContext) -> int:  
    query = update.callback_query

    context.bot.send_photo(chat_id=update.effective_user.id, photo=open(query.data + ".jpg",'rb'))

    context.bot.send_message(update.effective_user.id, "To start over enter /read or /delete")
    
    return ConversationHandler.END

def delete(update: Update, context: CallbackContext) -> int:

    show_list =[]
    file_names = os.listdir()
   
    for filename in file_names:
        if os.path.splitext(filename)[1] == '.jpg':
            show_list += [[InlineKeyboardButton(filename.rsplit('.')[0], callback_data = filename.rsplit('.')[0])]]
            
    show_markup = InlineKeyboardMarkup(show_list)

    update.message.reply_text("Click Button",reply_markup=show_markup)
    return DELETE_FILE

def delete_button(update: Update, context: CallbackContext) -> int:   
    query = update.callback_query

    os.remove(query.data + ".jpg")

    context.bot.send_message(update.effective_user.id, "Delete success \n\n To start over enter /read or /delete")
    
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('create', start_create)],
        states={
            RECV_IMAGE_NAME : [MessageHandler(Filters.text & ~Filters.command, recv_name)],
            RECV_IMAGE_FILE : [MessageHandler(Filters.photo, recv_image)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('read', read)],
        states={
            CLICK_BUTTON : [CallbackQueryHandler(read_button)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('delete', delete)],
        states={
            DELETE_FILE : [CallbackQueryHandler(delete_button)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))


    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
