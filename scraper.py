from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time

from utils.odds import calc_probs
from utils.scraping import get_soup
from utils.scraping import extract_snapshot


url = "https://sports.tipico.de/de/live/default"

soup = get_soup(url)

scraped_data = []

# Define the duration for which you want the script to run (in seconds)
duration =   60 # Run for 1 hour (adjust as needed)

# Start time
start_time = time.time()

# Main loop to scrape data
while time.time() - start_time < duration:
    # Your scraping logic here
    # For example, navigate to a webpage and scrape its content
    soup = get_soup(url)
    # Scraping code...
    # Store the scraped data in a dictionary or list
    snapshot_data = extract_snapshot(soup)
    scraped_data.append(snapshot_data)
    # Sleep for a certain interval before the next iteration
    time.sleep(10)  # Sleep for 10 seconds between iterations

# Close the web driver

# Convert the scraped data to a pandas DataFrame
#df = pd.DataFrame(scraped_data)

op_df = pd.concat(scraped_data, ignore_index=True)

print(op_df)

# Save the DataFrame to a CSV file

op_df.to_csv('scraped_data.csv', index=False)