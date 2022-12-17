import logging

from telegram import *
from telegram.ext import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CLICK_BUTTON,GET_NAME= range(2)

# Define a few command handlers. These usually take the two arguments update and
# context.
def getname(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('write your name')
    return GET_NAME

def name(update: Update, context: CallbackContext) -> None:
    """ GET_NAME 상태 """
    context.user_data['username'] = update.message.text
    #context.bot.send_message(context.user_data['username'] + " processed")
    update.message.reply_text(update.message.text + " processed")
    update.message.reply_text("To start over enter /name or /button")
    return ConversationHandler.END

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""   
    update.message.reply_text(update.message.text)

def cancel(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    
    context.user_data.clear()
    update.message.reply_text("Cancel!")
    return ConversationHandler.END


def inline_keyboard(update: Update, context: CallbackContext) -> None:
    context.user_data['telid'] = update.effective_user.id

    show_list =[[InlineKeyboardButton("button1",callback_data="button1")],
                [InlineKeyboardButton("button2",callback_data="button2")]]
    show_markup = InlineKeyboardMarkup(show_list)


    update.message.reply_text("Click Button",reply_markup=show_markup)


    return CLICK_BUTTON

def send_img(update: Update, context: CallbackContext):
    query = update.callback_query
    name_ = context.user_data['telid']
    if query.data == "button1":
        context.bot.send_photo(chat_id=update.effective_user.id,photo=open("index.jpg",'rb'))
        update.callback_query.message.edit_text(f"{name_} : Button1 img")
    elif query.data == "button2":
        context.bot.send_photo(chat_id=update.effective_user.id,photo=open("img.jpg",'rb'))
        update.callback_query.message.edit_text(f"{name_} : Button2 img")
    else :
        update.message.reply_text("To start over enter /name or /button")
    
    context.bot.send_message(update.effective_user.id, "To start over enter /name or /button")
    return ConversationHandler.END

RECV_IMAGE_NAME, RECV_IMAGE_FILE = (0, 1)

def start_create(update: Update, context: CallbackContext):
    update.message.reply_text("Enter image name")
    return RECV_IMAGE_NAME

def recv_name(update: Update, context: CallbackContext):
    context.user_data['filename'] = update.message.text
    update.message.reply_text(f"You have entered {context.user_data['filename']}")
    return RECV_IMAGE_FILE

def recv_image(update: Update, context: CallbackContext):
    print("!")
    file_id = update.message.photo[-1].file_id
    file = context.bot.getFile(file_id)
    file.download(f"{context.user_data['filename']}")
    
    text = "Upload success\n\n-> If you want to check a upload work?\n-> click the /read !!"
    context.bot .send_message(update.effective_user.id, text =text)

    return ConversationHandler.END

def read(update: Update, context: CallbackContext) -> None:
    ###
    # DB 혹은 csv형태로 저장된 key와 파일경로 
    ###
    context.bot.send_photo(chat_id=update.effective_user.id, photo=open("abc.jpg",'rb'))
    
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

    dispatcher.add_handler(CommandHandler('read', read))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    '''
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('name',getname)],
        states={

            GET_NAME : [MessageHandler(Filters.text & ~Filters.command, name)]

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))


    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('button',inline_keyboard)],
        states={

            CLICK_BUTTON : [CallbackQueryHandler(send_img)]

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))
    '''

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if name == '__main__':
    main()
