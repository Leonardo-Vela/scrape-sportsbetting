from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time

from utils.odds import calc_probs


def get_soup(url):
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    # Create a new instance of the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    # Navigate to the URL
    print("Preparing soup ...")
    driver.get(url)
    # Retrieve page source code 
    page_source = driver.page_source
    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()
    return soup 


def extract_snapshot(soup):
    # Get all "live" Event <a><a> elements
    event_tags = []
    try:
        live_events = soup.select_one('div.Program-styles-module-desktop')
        event_tags = live_events.select('a.EventRow-styles-module-event-row')
    except:
        pass
    print("Tasting soup ...")
    # Extract text content from each anchor tag
    # match time: xth minute
    # event name: "team A_versus_team B"
    # timestamp: 
    # odds: 
    # probabilities:
    # score:
    #columns = ['primary_key', 'name_team_A', 'name_team_B', 'gametime', 'score_team_A', 'score_team_B', 'odd_win_team_A', 'odd_draw', 'odd_win_team_B']
    data = []
    if len(event_tags) != 0:
        print("Tastes good !!!")
        for event in event_tags:
            try:
                team_names= event.select('span.EventTeams-styles-module-team-title')
                #print(team_names)
                score_tags = event.select_one('div.EventScores-styles-module-scores')
                score_list = [char for char in [score.get_text(strip=True) for score in  score_tags][-1]]
                team_names_list = [name.get_text(strip=True) for name in  team_names]
                event_id = str.replace(team_names_list[0] + "_versus_" + team_names_list[1], " ", "_")
                # Get current date and time
                current_datetime = datetime.datetime.now()
                current_date = datetime.date.today()
                current_time = datetime.datetime.now().time().strftime("%H:%M:%S")
                # Format the current datetime as a string
                datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                snapshot_id = event_id + "_time_" + datetime_string 
                #if len(event.select('div.EventDateTime-styles-module-live-date'))> 0:
                game_time_tag = event.select_one('div.EventDateTime-styles-module-info-cell-live')
                #print(game_time_tag)
                game_time = [game_time.get_text(strip=True) for game_time in  game_time_tag][0]
                #else
                odd_tags = event.select('div.EventOddGroup-styles-module-odd-group')
                odds_list = [1.0 if x == "" else float(x.replace(",",".")) for x in [odd.get_text(strip=True) for odd in  odd_tags[0]]]
                #print(odds_list)
                probs_list = calc_probs(odds_list)
                #print(probs_list)
                
                row_data = {
                    'primary_key': snapshot_id,
                    'match_key': event_id,
                    'date': current_date,
                    'time_of_day': current_time,
                    'name_team_A': team_names_list[0],
                    'name_team_B': team_names_list[1],
                    'gametime': game_time,
                    'score_team_A': score_list[0],
                    'score_team_B': score_list[1],
                    'odd_win_team_A': odds_list[0],
                    'odd_draw': odds_list[1],
                    'odd_win_team_B': odds_list[2],
                    'prob_win_team_A': probs_list[0],
                    'prob_draw': probs_list[1],
                    'prob_win_team_B': probs_list[2],
                    }
                
                data.append(row_data)
                
            except:
                pass

    df = pd.DataFrame(data)
    return df