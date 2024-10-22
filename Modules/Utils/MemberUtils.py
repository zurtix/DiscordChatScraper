from .Common import to_file

import re
import pandas as pd
import os
import csv 

ele = {
    "name" : "^name-",
    "activity": "activityText-",
    "avatar" : "^avatar-",
    "bot": "^botTag-",
    "member": "member-3-YXUe",
    "group": "membersGroup-v9BXpm"
}

def get_member_name(m):
    user = m.find("div", class_=re.compile(ele["name"]))
    return "" if user is None else user.text

def get_member_activity(m):
    activity = m.find("div", class_=re.compile(ele["activity"]))
    return "" if activity is None else activity.text

def get_member_id(m):
    avatar = m.find("img", class_=re.compile(ele["avatar"]))
    aregex = re.compile("\\d{18}")

    if avatar is not None:
        match = aregex.search(avatar.get("src"))
        if match is not None:
            return match.group()
    return ""

def get_member_group(m):
    if m is not None:
        if "offline" in m.text.lower():
            return ""
        else:
            return re.sub("\\d+$", "", m.text)[:-1]

def get_member_type(m):
    tag = m.find("span", class_=re.compile(ele["bot"]))
    return "USER" if tag is None else "BOT"

def get_member_index(m):
    return int(m.get("index"))

def get_members(html, stop=0): 

    collection = html.find_all(["div", "h2"])

    if collection is None:
        return

    df = pd.DataFrame()

    group = None

    for element in collection:

        if element is None:
            pass
        
        if (
            element.name == "div" and 
            element.get("class") is not None and
            ele["member"] in element.get("class")
        ):
            idx = get_member_index(element)
            id = get_member_id(element)
            user = get_member_name(element)
            utype = get_member_type(element)
            activity = get_member_activity(element)

            if idx > stop:

                data = ({"userid": id, 
                            "user": user, 
                            "type" : utype,
                            "activity" : activity,
                            "group" : group
                        })

                df = df.append(data, ignore_index=True)
        
        if (
            element.name == "h2" and 
            element.get("class") is not None and
            ele["group"] in element.get("class")          
        ):
            group = get_member_group(element)

    return idx, df

def dump(members, output, fmt, fltr=None):
    if len(members.index) == 0:
        return

    print(f"Writing {len(members.index)} lines to {output}_users")
    
    to_file(members, f"{output}_users.{fmt}", fmt)