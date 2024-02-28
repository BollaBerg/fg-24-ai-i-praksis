import os
from slack_bolt import App
from websockets.sync.client import connect
from hello_world import send_message
import json

app = App()

def open_socket():
    token = os.environ.get("SLACK_APP_LEVEL_TOKEN")
    return app.client.apps_connections_open(app_token=token)

def listen_for_events(url, should_reply):
    with connect(url) as websocket:
        while(True):
            message = json.loads(websocket.recv())
            print("MESSAGE: ", message)
            try:
                event = message["payload"]["event"]
                if should_reply(event["text"]):
                    channel_id = event["channel"]
                    ts = event["ts"]
                    send_message("Pong (take that!)", channel_id, ts)
            except Exception as e:
                print(e)
        

def listen_for_text(wanted_text):
    def listener(message):
        if wanted_text in message:
            return True
    return listener

if __name__ == "__main__":
    result = open_socket()
    print(result)
    
    if result.get("ok"):
        listen_for_events(result.get("url"), listen_for_text("Ping"))

    