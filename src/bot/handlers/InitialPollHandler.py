from telegram import Update, ReplyKeyboardMarkup, Bot
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, filters, ContextTypes
from backend.PollManager import PollManager
from model.Poll import createPoll, PollType
from utils.Commons import poll_reply_markup

FILLING_POLL_REPLY_MARKUP = ReplyKeyboardMarkup(
    [
        ["finish", "restart"],
        ["cancel"]
    ], one_time_keyboard=True
)

FINISH_POLL_REPLY_MARKUP = ReplyKeyboardMarkup(
    [["yes", "no"]], one_time_keyboard=True
)


class InitialPollHandler(ConversationHandler):

    def __init__(self, token: str, club_id: str, admin_id: str, poll_manager: PollManager):
        self.books: list[str] = []
        self.club_id, self.admin_id = club_id, admin_id
        self.poll_manager = poll_manager
        self.FILLING_POLL, self.FINISHED_FILLING = range(2)
        self.bot = Bot(token)
        super().__init__(
            entry_points=[CommandHandler(
                "create_first_poll", self.create_poll)],
            states={
                self.FILLING_POLL: [
                    MessageHandler(filters.Text(
                        ["finish"]), self.finish_filling),
                    MessageHandler(filters.Text(
                        ["restart"]), self.create_poll),
                    MessageHandler(filters.TEXT & ~
                                   filters.COMMAND, self.process_book),
                ],
                self.FINISHED_FILLING: [
                    MessageHandler(filters.Text(["yes"]), self.publish_poll),
                    MessageHandler(filters.Text(["no"]), self.create_poll)
                ]
            },
            fallbacks=[MessageHandler(filters.Text(
                ["cancel"]), self.cancel_creating_poll)]
        )

    async def create_poll(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        self.books.clear()
        await update.message.reply_text(
            "Введи название книги! Чтобы завершить, введи 'finish', чтобы отменить - 'cancel'",
            reply_markup=FILLING_POLL_REPLY_MARKUP
        )
        return self.FILLING_POLL

    async def finish_filling(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(
            "Зарегистрировали следующие книги: \n" +
            "\n".join(self.books) + "\nПодтверди!",
            reply_markup=FINISH_POLL_REPLY_MARKUP
        )
        return self.FINISHED_FILLING

    async def process_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        book = update.message.text
        self.books.append(book)
        await update.message.reply_text(
            "Книга '" + book + "' зарегистрирована!",
            reply_markup=FILLING_POLL_REPLY_MARKUP
        )
        return self.FILLING_POLL

    async def publish_poll(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        pollMessage = await self.bot.sendMessage(
            chat_id=self.club_id,
            text="Варианты!\n\n" + "\n".join(self.books),
            reply_markup=poll_reply_markup(self.books)
        )
        # send this poll to backend
        poll = createPoll(str(pollMessage.message_id),
                          PollType.INITIAL, self.books)
        self.poll_manager.save_poll(poll.id, poll.type, self.books)
        await self.bot.sendMessage(
            chat_id=self.admin_id,
            text="Опрос создан!"
        )
        await self.bot.forwardMessage(
            chat_id=update.message.chat.id,
            from_chat_id=self.club_id,
            message_id=pollMessage.message_id
        )
        return ConversationHandler.END

    async def cancel_creating_poll(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        self.books.clear()
        await update.message.reply_text("Ну и пошел нахуй!")
        return ConversationHandler.END
