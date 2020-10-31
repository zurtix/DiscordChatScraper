from time import sleep
from bs4 import BeautifulSoup
from .Utils.MemberUtils import get_members, dump

import pandas as pd
import re


class MemberWindow():
    def __init__(self, driver, speed):
        self.driver = driver
        self.speed = speed
        self.channel = None

    def scroll(self, channel):
        try:
            self.driver.execute_script(f"document.getElementById('members-{self.channel}').scrollBy(0, 1000);")
        except Exception as err:
            print(str(err)) 

    def bottom(self):
            self.driver.execute_script(f"""
            return document.getElementById('members-{self.channel}').scrollHeight 
            - document.getElementById('members-{self.channel}').scrollTop 
            - document.getElementById('members-{self.channel}').clientHeight < 1 ? 1 : 0""")

    def refresh(self):
        return BeautifulSoup(self.driver.find_element_by_id(f"members-{self.channel}")
            .get_attribute("innerHTML"), "html.parser")

    def members(self, output, channel, fmt, fltr=None):
        sleep(5)

        self.channel = channel

        stop = None
        temp = None

        while not self.bottom():
            data = self.refresh()
            members = get_members(data, stop)

            if members.equals(temp) or len(members.index) == 0:
                break

            print(members.iloc[0])

            stop = members.iloc[0]["user"]
            temp = members

            dump(members, output, fmt, fltr)

            self.scroll(channel)
            sleep(self.speed)