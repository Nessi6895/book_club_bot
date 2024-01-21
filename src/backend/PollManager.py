import requests
import json

from model.Poll import Poll, PollType, createPoll


class PollManager:
    def __init__(self, host: str) -> None:
        self.host = host

    def get_poll(self, poll_id: str) -> Poll:
        content = requests.get(self.host + "/polls/" + poll_id).content
        js = json.loads(content)
        type = PollType[str(js["type"]).upper()]
        answers: dict[str, list[str]] = js["answers"]
        not_reading: list[str] = js["notReading"]
        return Poll(poll_id, type, answers, not_reading)

    def vote(self, poll_id, voter, option) -> None:
        payload = {
            'pollId': poll_id,
            'voter': voter,
            'option': option
        }
        requests.post(self.host + "/polls/vote", data=json.dumps(payload))

    def not_reading(self, poll_id, voter) -> None:
        payload = {
            'pollId': poll_id,
            'voter': voter
        }
        requests.post(self.host + "/polls/skip", data=json.dumps(payload))
        

    def save_poll(self, poll_id, type: PollType, options: "list[str]") -> Poll:
        payload = {
            'pollId': poll_id,
            'type': type.name.lower().capitalize(),
            'options': options
        }
        r = requests.post(self.host + "/polls/new", data=json.dumps(payload))
        return createPoll(poll_id, type, options)

    def close_poll(self, poll_id: str) -> None:
        requests.delete(self.host + "/polls/"+ poll_id)
        
