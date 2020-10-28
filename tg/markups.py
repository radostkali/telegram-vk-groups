from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


CMD_ADD = '_add'
CMD_REMOVE = '_remove'
CMD_LIST = '_list'
CMD_DONE = '_done'

menu = ReplyKeyboardMarkup(
    [[KeyboardButton('/options')]],
    resize_keyboard=True,
)

options_buttons = [
    [InlineKeyboardButton('Add public', callback_data=CMD_ADD),
     InlineKeyboardButton('Remove public', callback_data=CMD_REMOVE)],
    [InlineKeyboardButton('List publics', callback_data=CMD_LIST)],
]
options_markup = InlineKeyboardMarkup(options_buttons, one_time_keyboard=True)

done_buttons = [
    [InlineKeyboardButton('Finish', callback_data=CMD_DONE)],
]
done_markup = InlineKeyboardMarkup(done_buttons, one_time_keyboard=True)


def get_comment_markup(pub_id: int, post_id: int) -> InlineKeyboardMarkup:
    btn = [[InlineKeyboardButton(
        text='See comments',
        url='https://vk.com/wall-{}_{}'.format(pub_id, post_id),
    )]]
    markup = InlineKeyboardMarkup(btn)
    return markup
