import os
from bot.BookClubBot import BookClubBot


API_TOKEN = os.environ["API_TOKEN"]
ADMIN_USER_ID = os.environ["ADMIN_USER_ID"]
CLUB_CHAT_ID = os.environ["CLUB_CHAT_ID"]


def main() -> None:
    BookClubBot(API_TOKEN, ADMIN_USER_ID, CLUB_CHAT_ID).run()


if __name__ == "__main__":
    main()
