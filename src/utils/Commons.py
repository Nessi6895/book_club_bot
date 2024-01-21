from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from model.CallbackData import CallbackData, CallbackType


def poll_reply_markup(options: "list[str]") -> InlineKeyboardMarkup:
    def option_to_button(option: str) -> InlineKeyboardButton:
        callback: str = CallbackData(CallbackType.BOOK_VOTE, {
                                     "book": option}).to_json()
        return InlineKeyboardButton(option, callback_data=callback)
    book_buttons = [[option_to_button(option)]
                    for i, option in enumerate(options)]
    not_reading_button = [[InlineKeyboardButton(
        'Не читаю', callback_data=CallbackData(CallbackType.NOT_READING).to_json())]]
    return InlineKeyboardMarkup(
        # should use better callback_data
        book_buttons + not_reading_button
    )
