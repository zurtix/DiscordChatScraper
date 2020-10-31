from .Common import to_file

import re
import pandas as pd
import os
import csv 

def get_member_name(m):
    user = m.find("div", class_=re.compile("^name-"))
    return "" if user is None else user.text

def get_member_activity(m):
    activity = m.find("div", class_=re.compile("activityText-"))
    return "" if activity is None else activity.text

def get_member_id(m):
    avatar = m.find("img", class_=re.compile("^avatar-"))
    aregex = re.compile("\d{18}")

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
            return re.sub("\d+$", "", m.text)[:-1]

def get_member_type(m):
    tag = m.find("span", class_=re.compile("^botTag-"))
    return "USER" if tag is None else "BOT"

def get_members(html, stop=None): 

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
            "member-3-YXUe" in element.get("class")
        ):
            id = get_member_id(element)
            user = get_member_name(element)
            utype = get_member_type(element)
            activity = get_member_activity(element)

            if user == stop:
                break

            data = ({"userid": id, 
                        "user": user, 
                        "type" : utype,
                        "activity" : activity,
                        "group" : group
                    })

            df = df.append(data, ignore_index=True)
        
        if element.name == "h2":
            group = get_member_group(element)


    return df

def dump(members, output, fmt, fltr=None):
    if len(members.index) == 0:
        return

    print(f"Writing {len(members.index)} lines to {output}_users")
    
    to_file(members, f"{output}_users.{fmt}", fmt)