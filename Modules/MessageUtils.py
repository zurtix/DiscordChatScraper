from .Common import to_file
from bs4 import BeautifulSoup
from time import sleep

import re
import pandas as pd



def get_message_text(m):
    return m.find("div", class_=re.compile("messageContent-"))

def get_message_id(m):
    return m.get("id").replace("chat-messages-", "")

def get_message_user(m):
    user = m.find("span", class_=re.compile("username-"))
    return "" if user is None else user.text

def get_message_user_id(m):
    avatar = m.find("img", class_=re.compile("^avatar-"))
    aregex = re.compile("\d{18}")

    if avatar is not None:
        match = aregex.search(avatar.get("src"))
        if match is not None:
            return match.group()
    return ""

def get_message_date(message):
    return ""

def get_messages(html, stop=None): 

    collection = html.find_all("div", id=re.compile("^chat-messages-"))

    if collection is None:
        return

    df = pd.DataFrame()

    tempU = None
    tempI = None

    for message in collection:
        mesgid = get_message_id(message)
        mesg = get_message_text(message)
        user = get_message_user(message)
        dt = get_message_date(message)
        id = get_message_user_id(message)

        if mesgid == stop:
            break

        if not user and not id:
            user = tempU
            id = tempI
        else:
            tempU = user
            tempI = id

        data = ({"userid": id, 
                    "user": user, 
                    "messageid" : mesgid,
                    "messagedate": dt,
                    "message": mesg.text.replace("\n", " ")
                })

        df = df.append(data, ignore_index=True)

    return df

def dump(messages, output, fmt, fltr=None):
    if len(messages.index) == 0:
        return

    if fltr is not None:
        if fltr[0] is not None:
            messages = messages[messages.user == fltr[0]]
        if fltr[1] is not None:
            messages = messages[messages["message"].str.contains(fltr[1])]

    print(f"Writing {len(messages.index)} lines to {output}")

    messages = messages[::-1]
    
    to_file(messages, f"{output}.{fmt}", fmt)