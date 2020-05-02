from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


CMD_ADD = 'add'
CMD_REMOVE = 'remove'
CMD_UPDATE = 'update'

menu = ReplyKeyboardMarkup(
    [[KeyboardButton('/options')]],
    resize_keyboard=True,
)

options_buttons = [
    [InlineKeyboardButton('Add public', callback_data=CMD_ADD),
     InlineKeyboardButton('Remove public', callback_data=CMD_REMOVE)],
    [InlineKeyboardButton('Check for new posts', callback_data=CMD_UPDATE)],
]
options_markup = InlineKeyboardMarkup(options_buttons, one_time_keyboard=True)

