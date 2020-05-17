from telegram.update import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
)

from tg.utils import (
    handle_public_link,
    check_or_create_user_in_db,
    link_public_to_user_in_db,
    list_user_publics,
    remove_public_by_number,
)
from tg.markups import (
    menu,
    options_markup,
    done_markup,
)
from tg.markups import (
    CMD_ADD,
    CMD_REMOVE,
    CMD_LIST,
    CMD_DONE,
)

STAGE_LISTENING = 0  # User si not in any action
STAGE_ADDING = 1  # User is adding publics to his list
STAGE_DELETING = 2  # User is picking public number to delete


def start(update, context):
    # type: (Update, CallbackContext) -> None
    update.message.reply_text('Hi there!', reply_markup=menu)
    update.message.reply_text('You can now create your publics list!', reply_markup=options_markup)
    context.user_data.update({'stage': STAGE_LISTENING})
    check_or_create_user_in_db(update.effective_chat.id)


def options(update, context):
    # type: (Update, CallbackContext) -> None
    update.message.reply_text('Choose what to do', reply_markup=options_markup)
    context.user_data.update({'stage': STAGE_LISTENING})


def button(update, context):
    # type: (Update, CallbackContext) -> None
    query = update.callback_query
    query.answer()
    opt = query.data
    if opt == CMD_ADD:  # Adding publics
        context.user_data.update({'stage': STAGE_ADDING})
        context.bot.send_message(chat_id=update.effective_chat.id, text='Paste public url or id:')
    if opt == CMD_REMOVE:  # Remove public from feed
        context.user_data.update({'stage': STAGE_DELETING})
        msg = 'Type public\'s number to remove:\n'
        publics = list_user_publics(update.effective_chat.id)
        if not publics:
            publics = '\tNo publics here yet. Add some first.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg + publics, reply_markup=done_markup)
    if opt == CMD_LIST:  # List user's publics
        context.user_data.update({'stage': STAGE_LISTENING})
        msg = 'Your publics:\n'
        publics = list_user_publics(update.effective_chat.id)
        if not publics:
            publics = '\tNo publics here yet. Add some first.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg + publics)
    if opt == CMD_DONE:  # Stop actions
        context.user_data.update({'stage': STAGE_LISTENING})
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ok, enjoy your news feed.')


def text_input(update, context):
    # type: (Update, CallbackContext) -> None
    if 'stage' not in context.user_data:
        return
    if context.user_data['stage'] == STAGE_ADDING:
        public_info = handle_public_link(update.message.text)
        if public_info:
            link_public_to_user_in_db(
                user_id=update.message.from_user.id,
                public_info=public_info
            )
            update.message.reply_text('Good! Another one?', reply_markup=done_markup)
        else:
            update.message.reply_text('Wrong url or public id! Try again:', reply_markup=done_markup)
    if context.user_data['stage'] == STAGE_DELETING:
        try:
            public_num = int(update.message.text)
        except ValueError:
            update.message.reply_text('Sike, that\'s the wrong number, try again:', reply_markup=done_markup)
        else:
            removed = remove_public_by_number(
                user_id=update.message.from_user.id,
                pub_num=public_num,
            )
            if not removed:
                msg = 'Sike, that\'s the wrong number, try again:\n'
                publics = list_user_publics(update.effective_chat.id)
                if not publics:
                    publics = '\tNo publics here yet. Add some first.'
                update.message.reply_text(msg + publics, reply_markup=done_markup)
            else:
                publics = list_user_publics(update.effective_chat.id)
                if not publics:
                    publics = '\tNo publics here yet. Add some first.'
                msg = '<b>{}</b> removed.\n' \
                      'Remove another public? Type number:\n'.format(removed)
                update.message.reply_text(
                    msg + publics,
                    reply_markup=done_markup,
                    parse_mode='HTML'
                )


HANDLERS = (
    CommandHandler('start', start),
    CommandHandler('options', options),
    CallbackQueryHandler(button),
    MessageHandler(Filters.text, text_input),
)

