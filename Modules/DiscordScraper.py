import os
from selenium import webdriver
from .MessageWindow import MessageWindow
from .MemberWindow import MemberWindow
from .Common import load_config
from time import sleep

class DiscordScraper():
    def __init__(self, args):
        self.args = args
        self.config = load_config(self.args.config)

        if self.config is None:
            exit(-1)

        self.driver = webdriver.Firefox(executable_path=self.config["driver"])
        self.speed = self.args.speed
        #super().__init__(self.driver, self.args.speed)

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

    def launch(self, server, channel):
        self.driver.get(f"https://discord.com/channels/{server}/{channel}")
        self.login(self.config["credentials"]["email"], self.config["credentials"]["passw"])

    def run(self):

        for d in self.config["discord"]:
            server = d["server"]

            member_window = MemberWindow(self.driver, self.speed)
            message_window = MessageWindow(self.driver, self.speed)

            for channel in d["channels"]:
                print(f"Scraping https://discord.com/channels/{server}/{channel}")

                self.launch(server, channel)
                member_window.members(f"{self.args.output}{channel}", channel, self.args.format.lower())

                self.launch(server, channel)
                message_window.messages(f"{self.args.output}{channel}", 
                                self.args.format.lower(), [self.args.user, self.args.search])
       
        self.driver.close()