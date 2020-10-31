# DiscordChatScraper
Scrape discord chats through the web client
The purpose of this project is to pull chat logs where the discord api may not be available

### Firefox Drivers
* Obtain FireFox drivers here, https://github.com/mozilla/geckodriver/releases

### Step 1:
python3 -m pip install -r requirements.txt

  
### Step 2:
Modify the contents of the config.json to reflect the server to scrape

### Step 3:
python3 main.py [args]
  
#### Note
Chat logs will display in reverse due to the lazy loading that occurs within the web client

#### Features to come
* Message datetime stamps
* Bypass NSFW channel notice



#### Discord Chat Scraper - command line arguments


    -h, --help show this help message and exit
        
    -f FORMAT, --format FORMAT Format types are, csv or json, default=csv
        
    -o OUTPUT, --output OUTPUT Output directory of where to place results, required=True
        
    -s SEARCH, --search SEARCH Text to search for within messages
        
    -c CONFIG, --config CONFIG Path to config file, equired=True
     
    -u USER, --user USER  Retrieve only message by this user

    -p SPEED, --speed SPEED Sets number of seconds to wait between scrolling, may be required for slower connections

