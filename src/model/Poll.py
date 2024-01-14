from enum import Enum


class PollType(Enum):
    INITIAL = 1
    FINAL = 2


class Poll:
    def __init__(self, id: str, type: PollType, answers: "dict[str, list[str]]", not_reading: "list[str]") -> None:
        self.id = id
        self.type = type
        self.answers = answers
        self.not_reading = not_reading

    def get_options(self) -> "list[str]":
        return list(self.answers.keys())

    def short_desc(self) -> str:
        results = [book + ": " + str(len(voters))
                   for book, voters in self.answers.items()]
        not_reading = ["Не читаю: " + str(len(self.not_reading))]
        return "\n".join(results + not_reading)


def createPoll(id: str, type: PollType, options: "list[str]") -> Poll:
    answers = {option: [] for option in options}
    return Poll(id, type, answers, [])
