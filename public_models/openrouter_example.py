import requests

from dotenv import load_dotenv
import os


if __name__ == '__main__':
    load_dotenv()
    headers = {
        "Authorization": f"Bearer {os.getenv('OPEN_ROUTER_API_KEY')}",
        "HTTP-Referer": os.getenv('MY_SITE_URL'),  # Optional for tracking
        "X-Title": os.getenv('MY_APP_NAME'),      # Optional
    }
    json_payload = {
        "model": os.getenv('OPEN_ROUTER_MODEL'),  # Free Llama 3 model
        "messages": [
            {
                "role": "user",
                "content": "Explain quantum computing in simple terms."
            }
        ]
    }

    response = requests.post(
        url=os.getenv("OPEN_ROUTER_URL"),
        headers=headers,
        json=json_payload
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
