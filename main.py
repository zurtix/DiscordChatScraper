from Modules.DiscordScraper import DiscordScraper
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Discord Chat Scraper")
    parser.add_argument("-f", "--format", action="store", dest="format", help="Format types are, CSV, or JSON", required=True)
    parser.add_argument("-o", "--output", action="store", dest="output", help="Output directory of where to place results", required=True)
    parser.add_argument("-s", "--search", action="store", dest="search", help="Text to search for within messages")
    parser.add_argument("-c", "--config", action="store", dest="config", help="Path to config file", required=True)
    parser.add_argument("-u", "--user", action="store", dest="user", help="Retrieve only message by this user")

    args = parser.parse_args()
    DiscordScraper(args).run()
    