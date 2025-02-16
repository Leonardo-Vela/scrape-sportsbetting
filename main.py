from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time

from utils.scraping import get_soup
from utils.scraping import extract_snapshot
from scripts.database import write_to_db


url = "https://sports.tipico.de/de/live/default"


# Define the duration for which you want the script to run (in seconds)
duration =   120 * 60 # Run for 2 hours (adjust as needed)

# Start time
start_time = time.time()

# Main loop to scrape data
while time.time() - start_time < duration:

    time_left = round((duration - (time.time() - start_time))/60, 1)
    print(f"{time_left} minutes left")
    # Your scraping logic here
    # For example, navigate to a webpage and scrape its content
    soup = get_soup(url)
    # Scraping code...
    # Store the scraped data in a dictionary or list
    snapshot_df = extract_snapshot(soup)
    #snapshot_df = pd.DataFrame(snapshot_data)
    #scraped_data.append(snapshot_data)
    write_to_db(snapshot_df)
    # Sleep for a certain interval before the next iteration
    time.sleep(1)


