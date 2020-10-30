from time import sleep
from .MessageCollection import MessageCollection
from bs4 import BeautifulSoup

import csv
import re

class ChatWindow():
    def __init__(self):
        self.soup = None

    def scroll(self):
        try:
            self.driver.execute_script("return document.getElementsByClassName('scroller-2LSbBU')[0].scrollTo(0, 0)")
            sleep(0.5)
        except Exception as err:
            print(str(err)) 

    def top(self):
        return self.driver.execute_script("return document.getElementsByClassName('scroller-2LSbBU')[0].scrollTop < 1 ? 1 : 0")

    def refresh(self):
        self.soup = BeautifulSoup(self.driver.find_element_by_id("chat-messages")
            .get_attribute("innerHTML"), "html.parser")

    def messages(self, output, fmt, fltr):
        sleep(5)

        stop = None
        while not self.top():
            self.refresh()
            
            messages = MessageCollection(self.soup, stop)
            
            stop = messages[0]["messageid"]

            messages.dump(output, fmt, fltr)

            self.scroll()
