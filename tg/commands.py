from telegram.update import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)

from tg.utils import (
    handle_public_link,
    check_or_create_user_in_db,
    link_public_to_user_in_db
)
from tg.markups import menu, options_markup
from tg.markups import (
    CMD_ADD,
    CMD_REMOVE,
    CMD_UPDATE,
)

STAGE_LISTENING = 0  # User si not in any action
STAGE_ADDING = 1  # User is adding publics to his list


def start(update, context):
    # type: (Update, CallbackContext) -> None
    update.message.reply_text('Hi there!', reply_markup=menu)
    update.message.reply_text('You can now create your publics list!', reply_markup=options_markup)
    context.user_data.update({'stage': STAGE_LISTENING})
    check_or_create_user_in_db(update.message.from_user.id)


def options(update, context):
    # type: (Update, CallbackContext) -> None
    update.message.reply_text('Choose what to do', reply_markup=options_markup)
    context.user_data.update({'stage': STAGE_LISTENING})


def button(update, context):
    # type: (Update, CallbackContext) -> None
    query = update.callback_query
    query.answer()
    opt = query.data
    if opt == CMD_ADD:
        context.user_data.update({'stage': STAGE_ADDING})
        context.bot.send_message(chat_id=update.effective_chat.id, text='Paste public url or id:')


def text_input(update, context):
    # type: (Update, CallbackContext) -> None
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    if 'stage' not in context.user_data:
        return
    if context.user_data['stage'] == STAGE_ADDING:
        public_info = handle_public_link(update.message.text)
        if public_info:
            link_public_to_user_in_db(
                user_id=update.message.from_user.id,
                public_info=public_info
            )
            context.bot.send_message(chat_id=update.effective_chat.id, text='Good! Another one?')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Wrong url or public id! Try again:')


HANDLERS = (
    CommandHandler('start', start),
    CommandHandler('options', options),
    CallbackQueryHandler(button),
    MessageHandler(None, text_input),
)

