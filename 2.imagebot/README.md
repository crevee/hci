# HCI-ImgBot

### Example code
``` Python
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
    """Send a message when the command /start is issued."""
    context.user_data['username'] = update.message.text
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


    show_list =[[InlineKeyboardButton("button1",callback_data="button1")],[InlineKeyboardButton("button2",callback_data="button2")]]
    show_markup = InlineKeyboardMarkup(show_list)


    update.message.reply_text("Click Button",reply_markup=show_markup)


    return CLICK_BUTTON

def send_img(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    name_ = context.user_data['username']
    if query.data == "button1":
        context.bot.send_photo(chat_id=update.effective_user.id,photo=open("testimg1.png",'rb'))
        update.callback_query.message.edit_text(f"{name_} : Button1 img")
        return ConversationHandler.END
    elif query.data == "button2":
        context.bot.send_photo(chat_id=update.effective_user.id,photo=open("testimg2.png",'rb'))
        update.callback_query.message.edit_text(f"{name_} : Button2 img")
        return ConversationHandler.END
    else :
        return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("Your Token")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher



    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


```

## 실습 목표

1. Create , Read , Delete 가 가능한 사진 관리 챗봇 만들기

2. Telegram API 의 ConversationHandler을 이용한 챗봇 만들기

### 사진 관리 챗봇(Create, Read , Delete)

Command Function List

- command '/create'

![Pasted image 20220920192232](https://user-images.githubusercontent.com/89440450/191405832-35b757c0-1d00-43c0-a29c-a130cf8197a1.png)

- /create 요구사항

    - 사진이름 직접 지정 가능해야함
    - 작동 순서 : /create → 사진이름 → 사진 전송

- command '/read'

![Pasted image 20220920192534](https://user-images.githubusercontent.com/89440450/191405954-0aa2b5fc-056f-451c-94fe-36ffe216600a.png)

- /read 요구사항

    - 저장한 사진의 목록을 InlineKeyboard 을 사용하여 버튼 형태로 출력

    - 버튼에는 사진 이름이 출력되어야함

    - 버튼을 클릭하면 사진 이름에 맞는 사진을 챗봇이 보여줘야함

- command '/delete'
![Pasted image 20220920193234](https://user-images.githubusercontent.com/89440450/191406029-5e806097-1055-4dfb-b3c9-b23fb90a6b07.png)

- /delete 요구사항

    - 저장한 사진의 목록을 InlineKeyboard 을 사용하여 버튼 형태로 출력

    - 버튼에는 사진 이름이 출력되어야함

    - 버튼을 클릭하면 사진 이름에 맞는 사진이 삭제됨

    - /read 로 사진 목록에서 이름 사라진 것 확인 가능해야함


##### Conversation Handler
```Python

dispatcher.add_handler(ConversationHandler(
    entry_points=[CommandHandler('button',inline_keyboard)],
    states={
        CLICK_BUTTON : [CallbackQueryHandler(send_img)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
))

```
- entry_points : ConversationHandler가 작동하기 위한 트리거 역할을 하는 Handler

- states : ConversationHandler의 상태 , 지정된 상태에 진입하면 정해진 Handler 작동

- `return CLICK_BUTTION` : 코드 작동 시 STATE 가 넘어가며 연결된 Handler 작동

- `return ConversationHandler.END` : 코드 작동시 작동중이던 ConversationHandler 종료

- fallback : ConversationHandler 강제종료를 위한 Handler


##### InlineKeyboard code

```Python

def inline_keyboard(update: Update, context: CallbackContext) -> None:
    show_list =[[InlineKeyboardButton("button1",callback_data="button1")]]
    show_markup = InlineKeyboardMarkup(show_list)
    update.message.reply_text("Click Button",reply_markup=show_markup)

return CLICK_BUTTON

```

- 주로 `CallbackQueryHandler` 와 같이 사용됨

- `[InlineKeyboardButton("button1",callback_data="button1")]` : 버튼에 표현될 내용과 버튼 클릭 시 넘어갈 데이터(`callback_data`)
