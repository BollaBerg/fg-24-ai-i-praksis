import os
import random

from slack_bolt import App
from websockets.sync.client import connect
from hello_world import send_message
import json
import pandas as pd
from pathlib import Path

app = App()


def open_socket():
    token = os.environ.get("SLACK_APP_LEVEL_TOKEN")
    return app.client.apps_connections_open(app_token=token)


def listen_for_events(url, should_reply):
    with connect(url) as websocket:
        while True:
            message = json.loads(websocket.recv())
            print("MESSAGE: ", message)
            try:
                websocket.send(json.dumps({"envelope_id": message["envelope_id"]}))
                event = message["payload"]["event"]
                if should_reply(event["text"]):
                    channel_id = event["channel"]
                    ts = event["ts"]
                    send_message("Pong (fra Andreas!)", channel_id, ts)
            except Exception as e:
                print("ERROR: ", e)
        

def listen_for_text(wanted_text):
    def listener(message):
        if wanted_text in message:
            return True
    return listener


def get_string_similarity(a: str, b: str):
    return random.random()


def get_closest_strings(data: pd.DataFrame, message: str, n_closest: int = 3):
    data["similarity"] = get_string_similarity(data["message"], message)
    return data.nlargest(n_closest, "similarity")


def get_data(data_path: Path = Path().absolute() / "data" / "processed" / "all_2023.txt"):
    return pd.read_csv(data_path, delimiter=",", quotechar="|", dtype="str")


if __name__ == "__main__":
    print(get_closest_strings(get_data(), "Hei, hva er skatt?", 5))
    # result = open_socket()
    # print(result)
    #
    # if result.get("ok"):
    #     listen_for_events(result.get("url"), listen_for_text("Ping"))

    