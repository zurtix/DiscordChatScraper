from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from Modules.MessageWindow import MessageWindow
from Modules.MemberWindow import MemberWindow
from Modules.Utils.Common import load_config
from bs4 import BeautifulSoup

import os
import re

ele = {
    "loginbtn" : "button-3k0cO7",
    "continuebtn" : "button.action-yrVND8.button-38aScr.lookFilled-1Gx00P.actionRed-gYn8D3.sizeLarge-1vSeWK.grow-q77ONN",
    "email" : "email",
    "pass": "password",
    "title": "title-1VcOOr"
}

class DiscordScraper():
    def __init__(self, args):
        self.args = args
        self.config = load_config(self.args.config)
        self.driver = webdriver.Firefox(executable_path=self.config["driver"])

    def login(self, e, p):
        try:
            email = self.driver.find_element_by_name(ele["email"])
            passw = self.driver.find_element_by_name(ele["pass"])
            submit = self.driver.find_element_by_class_name(ele["loginbtn"])
            
            email.send_keys(e)
            passw.send_keys(p)   
            
            submit.click()
            
            sleep(10)
        except:
            print("Login page not found!")

    def nsfw_check(self):
        bs = BeautifulSoup(self.driver.page_source, "html.parser")
        title = bs.find("div", class_=re.compile(ele["title"]))

        if "NSFW Channel" not in title.text:
            return

        button = self.driver.find_element_by_css_selector(ele["continuebtn"])
        button.click()


    def launch(self, server, channel):
        self.driver.get(f"https://discord.com/channels/{server}/{channel}")
        self.login(self.config["credentials"]["email"], self.config["credentials"]["passw"])
        self.nsfw_check()

    def run(self):

        for d in self.config["discord"]:
            server = d["server"]

            member_window = MemberWindow(self.driver, self.args.speed)
            message_window = MessageWindow(self.driver, self.args.speed)

            for channel in d["channels"]:
                print(f"Scraping https://discord.com/channels/{server}/{channel}")

                if self.args.skip:
                    self.launch(server, channel)
                    member_window.members(f"{self.args.output}{channel}", channel, self.args.format)

                self.launch(server, channel)
                message_window.messages(f"{self.args.output}{channel}", 
                                self.args.format, [self.args.user, self.args.search])
       
        self.driver.close()