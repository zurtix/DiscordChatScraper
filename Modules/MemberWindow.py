from time import sleep
from bs4 import BeautifulSoup
from Modules.Utils.MemberUtils import get_members, dump

import pandas as pd
import re


class MemberWindow():
    def __init__(self, driver, speed):
        self.driver = driver
        self.speed = speed
        self.channel = None

    def scroll(self):
        try:
            self.driver.execute_script(f"document.getElementById('members-{self.channel}').scrollBy(0, 1000);")
            sleep(self.speed)
        except Exception as err:
            print(str(err)) 

    def bottom(self):
            return self.driver.execute_script(f"""
            return document.getElementById('members-{self.channel}').scrollHeight 
            - document.getElementById('members-{self.channel}').scrollTop 
            - document.getElementById('members-{self.channel}').clientHeight < 1 ? 1 : 0""")

    def scroll_top(self):
        self.driver.execute_script(f"document.getElementById('members-{self.channel}').scrollTo(0, 0);")
        sleep(self.speed)

    def get_max_index(self):
        self.driver.execute_script(f"""document.getElementById('members-{self.channel}').scrollBy(0, 
                                    document.getElementById('members-{self.channel}').scrollHeight);""")
        sleep(self.speed)

        data = self.refresh()
        idx, _ = get_members(data)

        self.scroll_top()

        return int(idx)

    def refresh(self):
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def members(self, output, channel, fmt, fltr=None):
        sleep(5)
        
        self.channel = channel

        idx = -1
        last = self.get_max_index()

        while idx < last:
            data = self.refresh()
            idx, members = get_members(data, idx)

            dump(members, output, fmt, fltr)
            self.scroll()