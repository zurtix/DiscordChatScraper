import os
from selenium import webdriver
from .ChatWindow import ChatWindow
from .MemberWindow import MemberWindow
from .Utils import load_config
from time import sleep

class DiscordScraper(ChatWindow):
    def __init__(self, args):
        self.args = args
        self.config = load_config(self.args.config)

        if self.config is None:
            exit(-1)

        self.driver = webdriver.Firefox(executable_path=self.config["driver"])

        super().__init__(self.driver)

    def login(self, e, p):
        try:
            email = self.driver.find_element_by_name("email")
            passw = self.driver.find_element_by_name("password")
            email.send_keys(e)
            passw.send_keys(p)
            submit = self.driver.find_element_by_class_name('button-3k0cO7')
            submit.click()
            self.driver.implicitly_wait(10)
        except:
            print("Login page not found!")

    def run(self):
        try:
            if not os.path.exists(self.args.output):
                os.makedirs(self.args.output)
        except Exception as e:
            print(f"Error Occured: {type(e).__name__} {e.args}")
            exit(-1)

        for d in self.config["discord"]:
            server = d["server"]
            for channel in d["channels"]:
                print(f"Scraping https://discord.com/channels/{server}/{channel}")
                self.driver.get(f"https://discord.com/channels/{server}/{channel}")
                self.login(self.config["credentials"]["email"], 
                       self.config["credentials"]["passw"])
                #self.members()
                self.messages(f"{self.args.output}{channel}", 
                                self.args.format.lower(), [self.args.user, self.args.search])
       
        self.driver.close()