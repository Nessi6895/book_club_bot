from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def poll_reply_markup(options: "list[str]") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        # should add "Not reading" button
        # should have special callback_data (ex. "-1")
        # should use better callback_data
        [[InlineKeyboardButton(b, callback_data=str(b))]
         for i, b in enumerate(options)]
    )
