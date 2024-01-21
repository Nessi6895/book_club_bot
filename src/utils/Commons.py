from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def poll_reply_markup(options: "list[str]") -> InlineKeyboardMarkup:
    book_buttons = [[InlineKeyboardButton(b, callback_data=str(b))]
         for i, b in enumerate(options)]
    not_reading_button = [[InlineKeyboardButton('Не читаю', callback_data=-1)]]
    return InlineKeyboardMarkup(
        # should use better callback_data
        book_buttons+not_reading_button 
    )
