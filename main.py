from Modules.DiscordScraper import DiscordScraper
from Modules.Utils.Common import check_positive, check_output, check_config, check_format
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Discord Chat Scraper")
    parser.add_argument("-f", "--format", action="store", dest="format", help="Format types are, CSV, or JSON", default="csv", type=check_format)
    parser.add_argument("-o", "--output", action="store", dest="output", help="Output directory of where to place results", required=True, type=check_output)
    parser.add_argument("-s", "--search", action="store", dest="search", help="Text to search for within messages")
    parser.add_argument("-c", "--config", action="store", dest="config", help="Path to config file", required=True, type=check_config)
    parser.add_argument("-u", "--user", action="store", dest="user", help="Retrieve only message by this user")
    parser.add_argument("-p", "--speed", action="store", dest="speed", help="Sets number of seconds to wait between scrolling, may be required for slower connections", type=check_positive)
    parser.add_argument("-x", "--skip-users", nargs="?", dest="skip", default=False)

    args = parser.parse_args()
    DiscordScraper(args).run()
    