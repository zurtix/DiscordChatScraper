from bs4 import BeautifulSoup
from time import sleep
import re
import pandas as pd
import csv
import os



class MessageCollection():
    def __init__(self, soup, stop):
        self.collection = None
        self.stop = stop
        self.df = pd.DataFrame()
        self.load(soup)
        self.get_message()

    def __getitem__(self, key):
        if len(self.df.index) > 0:
            value = self.df.iloc[key]
            return value

    def __iter__(self):
        return (
            item
            for item in self.df[::-1].iterrows()
        )

    def load(self, soup):
        self.collection = soup.find_all("div", id=re.compile("^chat-messages-"))

    def get_user(self, m):
        user = m.find("span", class_=re.compile("username-"))
        return "" if user is None else user.text

    def get_text(self, m):
        return m.find("div", class_=re.compile("messageContent-"))

    def get_id_from_avatar(self, m):
        avatar = m.find("img", class_=re.compile("^avatar-"))
        aregex = re.compile("\d{18}")
        if avatar is not None:
            match = aregex.search(avatar.get("src"))
            if match is not None:
                return match.group()
        return ""

    def get_message_date(self, message):
        return ""

    def get_message(self): 
        if self.collection is None:
            return

        tempU = None
        tempI = None

        for message in self.collection:
            mesg = self.get_text(message)
            mesgid = message.get("id").replace("chat-messages-", "")
            user = self.get_user(message)
            dt = self.get_message_date(message)
            id = self.get_id_from_avatar(message)

            if mesgid == self.stop:
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

            self.df = self.df.append(data, ignore_index=True)

    def dump(self, output, fmt=None, fltr=None):
        if len(self.df.index) == 0:
            return

        if fltr is not None:
            if fltr[0] is not None:
                self.df = self.df[self.df.user == fltr[0]]
            if fltr[1] is not None:
                self.df = self.df[self.df["message"].str.contains(fltr[1])]

        print(f"Writing {len(self.df.index)} lines to file")

        self.df = self.df[::-1]
        
        if fmt == "csv":
            self.df.to_csv(f"{output}.csv", header=False,index=False, 
                  doublequote=True, quoting=csv.QUOTE_NONNUMERIC, mode="a")
        else:
            if not os.path.exists(f"{output}.json"):
                self.df.to_json(f"{output}.json",orient="records", lines=True)
            else:
                open(f"{output}.json", "a").write(self.df.to_json(orient="records", lines=True))