from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd


df_kickstarter = pd.read_csv('./Hans/Hans/kickstarter.csv')
# Filter rows based on column: 'project_country'
df_kickstarter = df_kickstarter[df_kickstarter['project_country'] == "US"]
# Filter rows based on column: 'project_currency'
df_kickstarter = df_kickstarter[df_kickstarter['project_currency'] == "USD"]
# Drop rows with missing data in column: 'project_title'
df_kickstarter = df_kickstarter.dropna(subset=['project_title'])
# Drop rows with missing data in column: 'project_description'
df_kickstarter = df_kickstarter.dropna(subset=['project_description'])

# Create new Grammarly Column
df_kickstarter['grammarly_performance'] = ""


# Set the path to your text files
text_files_path = 'C:/Uni/Bachelorthesis/txtfiles/'

# Get a list of all files in the directory
files = os.listdir(text_files_path)

# Sort the files based on their numerical value
sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))

# Set the path to your Chrome user profile directory
chrome_profile_path = 'C:/Users/hanso/AppData/Local/Google/Chrome/User Data'

# Specify the path to the ChromeDriver executable
chromedriver_path = 'C:/Uni/Bachelorthesis/chromedriver.exe'

# Create a Service object
service = Service(chromedriver_path)

# Set Chrome options to run in app mode
chrome_options = Options()
chrome_options.add_argument(f'--user-data-dir={chrome_profile_path}')
chrome_options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

# Initialize the Chrome WebDriver with the options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Loop through the text files and upload each file
for filename in sorted_files:

    # Navigate to Grammarly Editor
    driver.get('https://app.grammarly.com/')

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'upload')))

    # Find the file upload button
    upload_button = driver.find_element(By.ID, 'upload')

    file_path = os.path.join(text_files_path, filename)

    # Provide the file path to the file upload input field
    upload_button.send_keys(file_path)

    # Wait for the notification close icon to appear and click it
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'f2phmyy.notifications-closeIconWrapper_f7j52aq.f17uf1gk')))
    close_icon = driver.find_element(By.CLASS_NAME, 'f2phmyy.notifications-closeIconWrapper_f7j52aq.f17uf1gk')
    close_icon.click()

    # Wait for the done button to appear and click it
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'fqlvlsm.f2phmyy.fns4yay')))
    done_button = driver.find_element(By.CLASS_NAME, 'fqlvlsm.f2phmyy.fns4yay')
    done_button.click()

    # Extract the performance score
    performance_score_element = driver.find_element(By.CLASS_NAME, 'fal6plv.navigation-outcomeBtn_f160k9oy.navigation-outcomeBtnBorders_ffjervb._94f802ae-header-performanceBtnHigh._c37af1c2-header-headerBtn.f17uf1gk')
    performance_score_string = performance_score_element.get_attribute('aria-label')
    print(f'Performance score string for {filename}: {performance_score_string}')
    # Extract the performance score substring
    start_index = performance_score_string.index(':') + 1
    end_index = performance_score_string.index('%')
    performance_score = performance_score_string[start_index:end_index].strip()

    print(f'Performance score for {filename}: {performance_score}')
    df_kickstarter.at[int(filename.split('.')[0]), 'grammarly_performance'] = performance_score

# Quit the browser
driver.quit()

# Save the updated DataFrame to a CSV file
df_kickstarter.to_csv('kickstarter_grammarly.csv')