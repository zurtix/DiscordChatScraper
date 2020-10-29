import os
from selenium import webdriver
from .ChatWindow import ChatWindow
from .Utils import load_config

class DiscordScraper(ChatWindow):
    def __init__(self, args):
        self.args = args
        self.driver = None
        super().__init__()

    def login(self, e, p):
        email = self.driver.find_element_by_name("email")
        passw = self.driver.find_element_by_name("password")
        email.send_keys(e)
        passw.send_keys(p)
        submit = self.driver.find_element_by_class_name('button-3k0cO7')
        submit.click()
        self.driver.implicitly_wait(10)

    def run(self):
        config = load_config(self.args.config)

        self.driver = webdriver.Firefox(executable_path=config["driver"])

        try:
            if not os.path.exists(self.args.output):
                os.makedirs(self.args.output)
        except Exception as e:
            print("Unable to created output directory, please check your permissions")
            exit(-1)

        for d in config["discord"]:
            server = d["server"]
            for channel in d["channels"]:
                self.driver.get(f"https://discord.com/channels/{server}/{channel}")
                self.login(config["credentials"]["email"], 
                   config["credentials"]["passw"])
                self.messages(f"{self.args.output}{channel}", 
                                self.args.format, [self.args.user, self.args.search])
                
        self.driver.close()