from onepush import get_notifier
import os
from dotenv import load_dotenv

# this project will be using OnePush as the push notification service.

def test_notifier(provider:str, title:str, content:str):

    load_dotenv()
    n = get_notifier(provider)
    response = n.notify(
        key=os.getenv('BARK_KEY'), 
        title=title, 
        content=content
    )
    return response