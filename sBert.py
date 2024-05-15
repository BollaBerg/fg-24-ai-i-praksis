import os
import random

from slack_bolt import App
from websockets.sync.client import connect
from hello_world import send_message
import json
import pandas as pd
from pathlib import Path

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('models/221')


def open_socket():
    app = App()

    token = os.environ.get("SLACK_APP_LEVEL_TOKEN")
    return app.client.apps_connections_open(app_token=token)


def listen_for_events(url, get_reply):
    with connect(url) as websocket:
        while True:
            message = json.loads(websocket.recv())
            print("MESSAGE: ", message)
            try:
                websocket.send(json.dumps({"envelope_id": message["envelope_id"]}))
                event = message["payload"]["event"]
                channel_id = event["channel"]
                ts = event["ts"]
                if event.get("thread_ts", None) is None:
                    send_message(get_reply(event["text"]), channel_id, ts)
            except Exception as e:
                print("ERROR: ", e)


def listen_for_text(wanted_text):
    def listener(message):
        if wanted_text in message:
            return True

    return listener


def get_data(data_path: Path = Path().absolute() / "data" / "processed" / "all_top_2023.txt"):
    data_ = pd.read_csv(data_path, delimiter=",", quotechar="|", dtype="str").dropna(axis=0)
    data_["embedding"] = [model.encode(message) for message in data_['message']]
    return data_


if __name__ == "__main__":
    data = get_data()

    def get_reply_fn(new_message):
        encoded = model.encode(new_message)
        data["similarity"] = data["embedding"].apply(lambda emb: util.cos_sim(emb, encoded).item())
        reply_message = data.nlargest(1, 'similarity')
        return (f"This looks like the message: \n> {reply_message["message"].item()}\n"
                f"(ts: {reply_message["ts"].item()}, similarity: {reply_message["similarity"].item()})")

    result = open_socket()
    print(result)

    if result.get("ok"):
        listen_for_events(result.get("url"), get_reply_fn)
