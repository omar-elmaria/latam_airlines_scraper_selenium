# Import the libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

# Set the chrome options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) # Keep the browser open after the code terminates
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Suppress the warning messages

# Instantiate a browser object
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the URL
driver.get("https://www.latamairlines.com/us/en")

# Go to US site
driver.find_element(by=By.XPATH, value="//*[@id='country-suggestion-body-reject-change']/span").click()

# Maximize window
driver.maximize_window()

# Scrape information on the flight offers from Boston
def scrape_listings_func():
    flight_data_list = []
    for iter in range(2):
        flights = driver.find_elements(by=By.XPATH, value="//li[@width='426.6666666666667' and @aria-hidden='false']")
        for fl in flights:
            departure_date = fl.find_element(by=By.XPATH, value=".//span[contains(@id, 'deal-card-from')]").text
            
            return_date = fl.find_element(by=By.XPATH, value=".//span[contains(@id, 'deal-card-to')]").text
            
            destination = fl.find_element(by=By.XPATH, value=".//h3[@class = 'sc-drMfKT kpfDwt']").text

            deal_type = fl.find_elements(by=By.XPATH, value=".//div[contains(@id, 'detail-deal-tag')]")
            trip_type = deal_type[0].text
            flight_class = deal_type[1].text

            price = fl.find_element(by=By.XPATH, value=".//p[contains(@id, 'deal-card-primary-price')]").text
            price = re.findall(pattern="\d.+", string=price)
            try:
                price = price[0].replace(",", "")
            except IndexError:
                price = None # If the price does not exist, set the value to None

            flight_data_dict = {
                "departure_date": departure_date,
                "destination": destination,
                "return_date": return_date,
                "trip_type": trip_type,
                "flight_class": flight_class,
                "price": price
            }

            flight_data_list.append(flight_data_dict) # Append the dictionary to the list
            
        if iter == 1: # There are only 6 listings on the landing page, so break out of the loop after the second iteration
            break
        else:
            next_button = driver.find_element(by=By.XPATH, value="//button[@data-testid='deals-carousel-nextSlide-btn-icon-button']") # Find the next button
            for i in range(3):
                next_button.click() # Click 3 times until the other listings appear
                time.sleep(1) # Wait one second between each click 

    return flight_data_list

# Run the function and change the list to a dataframe
df_flight_data = pd.DataFrame(scrape_listings_func())
print(df_flight_data)

# Do some actions
# Origin
driver.find_element(by=By.XPATH, value="//input[@id='txtInputOrigin_field']").send_keys("Belo Horizonte, CNF - Brazil")
driver.find_element(by=By.XPATH, value="//*[@id='btnItemAutoComplete_0']").click()
time.sleep(1)

# # Destination
driver.find_element(by=By.XPATH, value="//*[@id='txtInputDestination_field']").send_keys("New York, JFK - United States")
driver.find_element(by=By.XPATH, value="//*[@id='btnItemAutoComplete_0']").click()
time.sleep(1)

# Check off "Use LATAM Miles"
driver.find_element(by=By.XPATH, value="//*[@id='get-redemption-checkbox']").click()
time.sleep(1)

# Departure date
driver.find_element(by=By.XPATH, value="//label[@for='departureDate']").click()
time.sleep(1)
driver.find_element(by=By.XPATH, value="//td[contains(@aria-label, 'December 2, 2022')]/span").click()
time.sleep(1)

# Return date
driver.find_element(by=By.XPATH, value="//td[contains(@aria-label, 'December 16, 2022')]/span").click()
time.sleep(1)

# Click "Search"
driver.find_element(by=By.XPATH, value="//*[@id='btnSearchCTA']").click()