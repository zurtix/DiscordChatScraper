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
            self.refresh()
            self.driver.execute_script("document.getElementsByClassName('scroller-2LSbBU')[0].scrollTo(0, 0);")
        except Exception as err:
            print(str(err)) 

    def top(self):
        if ( 
        self.soup.find("div", class_=re.compile("^emptyChannelIcon-")) 
        or self.soup.find("div", class_=re.compile("^inner-"))
        ):
            return True
        return False

    def refresh(self):
        self.soup = BeautifulSoup(self.driver.find_element_by_id("chat-messages")
            .get_attribute("innerHTML"), "html.parser")

    def messages(self, output, fmt, fltr):
        sleep(5)
        self.refresh()

        top = False
        stop = None

        while not top:
            sleep(2)
            self.scroll()

            messages = MessageCollection(self.soup, stop)
            stop = messages[0]["messageid"]
            messages.dump(output, fmt, fltr)

            top = self.top()