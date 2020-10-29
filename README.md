# DiscordChatScraper
Scrape discord chats

### Firefox Drivers
* Obtain FireFox drivers here, https://github.com/mozilla/geckodriver/releases

### Step 1:
Modify the contents of the config.json to reflect the server to scrape
  
### Step 2:
python3 main.py
  
#### Note
Chat logs will display in reverse due to the lazy loading that occurs within the web client

#### Features to come
* Message timestamps
* Bypass NSFW channel notice



#### Discord Chat Scraper - command line arguments


    -h, --help show this help message and exit
        
    -f FORMAT, --format FORMAT Format types are, CSV, or JSON **(Required)**
        
    -o OUTPUT, --output OUTPUT Output directory of where to place results **(Required)**
        
    -s SEARCH, --search SEARCH Text to search for within messages
        
    -c CONFIG, --config CONFIG Path to config file **(Required)**
     
    -u USER, --user USER  Retrieve only message by this user

