from telegram import Update
from telegram.ext import Application
from bot.handlers.InitialPollHandler import InitialPollHandler
from bot.handlers.ProcessVoteHandler import ProcessVoteHandler
from backend.PollManager import PollManager


class BookClubBot:
    def __init__(self, token: str, admin_id: str, club_id: str) -> None:
        poll_manager = PollManager("http://84.201.132.131:8080")
        self.application = Application.builder().token(token).build()
        self.application.add_handler(
            InitialPollHandler(token, club_id, admin_id, poll_manager))
        self.application.add_handler(ProcessVoteHandler(
            poll_manager))

    def run(self) -> None:
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
