import os
from slack_bolt import App
from slack_sdk import WebClient

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def send_message(message, channel_id = "C06MNH9JYJC", thread_ts = None):
    # Call the conversations.list method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts,
        text=message
    )
    print(result)


if __name__ == "__main__":
    send_message("Hello from Python!")