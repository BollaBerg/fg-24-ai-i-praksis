import os
from slack_bolt import App
from websockets.sync.client import connect
import time

app = App()

def open_socket():
    token = os.environ.get("SLACK_APP_LEVEL_TOKEN")
    return app.client.apps_connections_open(app_token=token)

def listen_for_events(url, event_type, callback):
    with connect(url) as websocket:
        while(True):
            message = websocket.recv()
            print(message)
        


if __name__ == "__main__":
    result = open_socket()
    print(result)
    
    if result.get("ok"):
        listen_for_events(result.get("url"), "", "")

    