from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from backend.PollManager import PollManager

from model.Poll import Poll
from utils.Commons import poll_reply_markup


class ProcessVoteHandler(CallbackQueryHandler):
    def __init__(self, poll_manager: PollManager):
        self.poll_manager = poll_manager
        super().__init__(callback=self.__vote_for_book)

    async def __vote_for_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        print(query.message.id)
        poll: Poll = self.poll_manager.get_poll(str(query.message.id))
        book: str = query.data
        voter = update.callback_query.from_user.username
        self.poll_manager.vote(poll.id, voter, book)
        print(poll.id)
        poll = self.poll_manager.get_poll(poll.id)
        await query.edit_message_text("Варианты:\n\n" + poll.short_desc(), reply_markup=poll_reply_markup(poll.get_options()))
