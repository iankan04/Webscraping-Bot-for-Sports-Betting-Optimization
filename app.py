import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import time
from datetime import date
import os
import random
import pandas as pd

def main():
    # The file path to the data folder
    filepath = "/Users/iank8/Desktop/Coding Projects/Sports Betting Stats/data"

    # The name of the CSV
    csv_name = get_current_formatted_date() + "_final" + ".csv"  

    # The file path with today's csv name appended
    named_filepath = filepath + "/" + csv_name

    # Append CSV file to data folder if not present
    if not contains_file(filepath, csv_name):
        dfProps = generate_database_from_PP()
        dfProps.to_csv(named_filepath, index=False)


def generate_database_from_PP():
    # proxy_ip_port = "159.192.138.170:8080"
    # config.proxy['https']
    # proxy_server = "https://" + proxy_ip_port

    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--deny-permission-prompts")
    # options.add_argument('--proxy-server=%s' % proxy_server)
    # options.add_experimental_option("detach", True)
    driver = uc.Chrome(options=options)

    # Scraping PrizePicks https://app.prizepicks.com/
    driver.get("https://app.prizepicks.com/")

    # Exits out of popup
    wait = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "close")))
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div/button").click()
    time.sleep(2)

    # Creating tables for players
    ppPlayers = []

    # Navigates to soccer tab
    driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='SOCCER']").click()
    time.sleep(2)

    # Waiting until stat_container is visible
    stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))
    
    # Finds all stat categories
    categories = driver.find_element(By.XPATH, '//*[@id="board"]/nav[2]/div').text.split('\n')

    for category in categories:
        driver.find_element(By.XPATH, f"//div[text()='{category}']").click()
        projectionsPP = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@aria-label='Projections List']")))
        
        for projection in projectionsPP:
            name = projection.find_element(By.ID, "test-player-name").text
            position = projection.find_element(By.ID, "test-team-position").text
            pts = projection.find_element(By.XPATH, "//*[@id='test-projection-li']/div[3]/div/div/div/div[1]").text
            proptype = projection.find_element(By.XPATH, "//*[@id='test-projection-li']/div[3]/div/div/div/div[2]").text

            player_prop = {
                "Name" : name,
                "Position" : position,
                "Points" : pts,
                "Proptype" : proptype
            }

            ppPlayers.append(player_prop)
    
    dfProps = pd.DataFrame(ppPlayers)
    return dfProps


def get_current_formatted_date():
    """
    Returns the today's date in the format: MM-DD-YY
    """
    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    return formatted_date


def contains_file (filepath, file_name):
    """
    Arguments:
        filepath=path to folder in directory
        file_name=name of file to be searched
    Returns a boolean whether the file "file_name" is in the folder at "filepath"
    """
    files_in_folder = os.listdir(filepath)
    return file_name in files_in_folder 


main()





