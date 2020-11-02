from .Common import to_file
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

import re
import pandas as pd

def get_message_text(m):
    message = m.find("div", class_=re.compile("messageContent-"))
    return message.text.replace("\n", " ")

def get_message_id(m):
    return m.get("id").replace("chat-messages-", "")

def get_message_user(m):
    user = m.find("span", class_=re.compile("username-"))
    return "" if user is None else user.text

def get_message_user_id(m):
    avatar = m.find("img", class_=re.compile("^avatar-"))
    aregex = re.compile("\\d{18}")

    if avatar is not None:
        match = aregex.search(avatar.get("src"))
        if match is not None:
            return match.group()
    return ""

def get_message_date(e):
    if e is None or not e.text :
        return datetime(1990, 1, 1)

    return datetime.strptime(e.text, "%B %d, %Y")

def get_message_time(m):
    time = m.find("span", class_=re.compile("timestamp-"))

    t = datetime(1990, 1, 1, 1, 1, 1)

    if time is None or not time.text:
        return t

    try:
        time = time.text
        time = time.replace("]", "")
        time = time.replace("[", "")
        return datetime.strptime(time.strip(), "%I:%M %p")
    except:
        return t
    

def get_message_full_date(date, time):

    d = datetime(1990, 1, 1)
    t = datetime(1990, 1, 1, 1, 1, 1)

    if date:
        d = date

    if time:
        t = time
 
    date_time = datetime.combine(d, t.time())
    return date_time.strftime("%Y-%m-%dT%H:%M:%S%z")

def get_messages(html, stop=None): 

    collection = html.find_all("div")

    if collection is None:
        return

    df = pd.DataFrame()

    temp_user = None
    temp_id = None
    temp_date = None

    for element in collection:
        if element is None:
            pass

        if (
            element.get("id") is not None and
            "chat-messages-" in element.get("id")
        ):
            mesgid = get_message_id(element)
            mesg = get_message_text(element)
            user = get_message_user(element)
            time = get_message_time(element)
            dt = get_message_full_date(temp_date, time)
            id = get_message_user_id(element)

            if mesgid == stop:
                break

            if not user and not id:
                user = temp_user
                id = temp_id
            else:
                temp_user = user
                temp_id = id

            data = ({"userid": id, 
                        "user": user, 
                        "messageid" : mesgid,
                        "messagedate": dt,
                        "message": mesg
                    })

            df = df.append(data, ignore_index=True)

        if (
            element.get("class") is not None and
            "divider-3_HH5L" in element.get("class")
        ):
            temp_date = get_message_date(element)

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