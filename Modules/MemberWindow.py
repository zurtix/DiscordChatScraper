import re
from time import sleep


class MemberWindow():
    def __init__(self):
        self.soup = None

    def scroll(self, channel):
        try:
            self.driver.execute_script(f"document.getElementsByClassName('members-{channel}')[0].scrollTo(0, 0);")
            sleep(0.5)
        except Exception as err:
            print(str(err)) 

    def bottom(self):
            self.driver.execute_script(f"""
            return document.getElementById('members-{channel}').scrollHeight 
            - document.getElementById('members-{channel}').scrollTop 
            - document.getElementById('members-{channel}').clientHeight < 1 ? 1 : 0""")

    def refresh(self):
        self.soup = BeautifulSoup(self.driver.find_element_by_id("menbers-")
            .get_attribute("innerHTML"), "html.parser")

    def members(self):
        sleep(5)

        stop = None
        while not self.top():
            self.refresh()       
            members = MemberCollection(self.soup, stop)            
            stop = members[0]["userid"]
            members.dump(f"{output}_users", fmt, fltr)
            self.scroll()
