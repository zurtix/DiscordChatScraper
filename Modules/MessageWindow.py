from time import sleep
from .MessageUtils import get_messages, dump
from bs4 import BeautifulSoup

import re

class MessageWindow():
    def __init__(self, driver, speed):
        self.driver = driver
        self.speed = speed

    def scroll(self):
        try:
            self.driver.execute_script("document.getElementsByClassName('scroller-2LSbBU')[0].scrollTo(0, 0)")
        except Exception as err:
            print(str(err)) 

    def refresh(self):
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def messages(self, output, fmt, fltr):
        sleep(5)

        stop = None
        temp = None

        while True:
            data = self.refresh()
            messages = get_messages(data, stop)

            if messages.equals(temp) or len(messages.index) == 0:
                # verify we didn't experience packet loss
                break

            stop = messages.iloc[0]["messageid"]
            temp = messages

            dump(messages, output, fmt, fltr)
            self.scroll()

            sleep(self.speed)
