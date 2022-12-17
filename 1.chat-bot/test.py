import telegram
import logging
import os, glob
import os.path

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#token = ''
#id = ''
#bot = telegram.Bot(token = token)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    print(update.message.chat_id)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')



def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""   
    tokens = update.message.text.split(" ")

    if( tokens[0] == "list_file"):
        #data = glob.glob("./tokens[1]")
        targerdir = r"/workspaces/chat-bot-Cre-Eve"

        def isStartWithF(x):
            return x.startswith(tokens[1])

        files = list(filter(isStartWithF, os.listdir(targerdir)))
        update.message.reply_text(files)
    else:
        update.message.reply_text(update.message.text)

def list_command(update: Update, context: CallbackContext) -> None:
    """list on document."""
    targerdir = r"/workspaces/chat-bot-Cre-Eve"
    files = os.listdir(targerdir)
    update.message.reply_text(files)
    


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5436263461:AAE4PFugz3N_7KnVkASk-LKgpTIWNhBE3uY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("list", list_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
