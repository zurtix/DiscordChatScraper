from time import sleep
from bs4 import BeautifulSoup
from Modules.Utils.MessageUtils import get_messages, dump

import re

ele = {
    "scroller" : "scroller-2LSbBU"
}

class MessageWindow():
    def __init__(self, driver, speed):
        self.driver = driver
        self.speed = speed

    def scroll(self):
        try:
            self.driver.execute_script(f"document.getElementsByClassName('{ele['scroller']}')[0].scrollTo(0, 0)")
            sleep(self.speed)
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

            if messages.equals(temp) or messages.empty:
                break

            stop = messages.iloc[0]["messageid"]
            temp = messages

            dump(messages, output, fmt, fltr)
            self.scroll()
