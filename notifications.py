import requests
from config import ntfy_topic

def send_notification(title, data):
    requests.post(
        f"https://ntfy.sh/{ntfy_topic}",
        data=data.encode('utf-8'),
        headers={
            "Title": title,       # Optional: Adds a bold title
            "Priority": "high",            # Optional: max, high, default, low, min
            "Tags": ""  # Optional: Adds emojis/icons
        }
    )

