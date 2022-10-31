from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# get the time and set a 5 sec an 5 min interval
check_supplies = time.time() + 5
end_game = time.time() + (60 * 5)

# get the safari driver to selenium
driver = webdriver.Safari()

# get the original version of the cookie page
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# get the cookie, and supply info to be use to click or gather info
cookie = driver.find_element(By.ID, "cookie")
supplies = driver.find_elements(By.CSS_SELECTOR, "#store div")
supplies_list = [supply.get_attribute("id") for supply in supplies]

# the program should run as long as it is below the end time
while time.time() < end_game:
    cookie.click()
    if time.time() > check_supplies:
        supply_prices = []
        supply_upgrades = {}
        possible_supply_upgrades = {}
        # get a list of the values of the price
        prices = driver.find_elements(By.CSS_SELECTOR, "#store b")

        # get the price of an item for each item from the list
        for price in prices:
            # get the texts for the number
            supply_text = price.text
            # as long as the the value isn't an empty string
            if supply_text != "":
                # get ride of the words like cost, the cookie image and , if in it
                cost = int(supply_text.split("-")[1].strip().replace(",", ""))
                # add the price to the list of prices
                supply_prices.append(cost)


        for n in range(len(supply_prices)):
            # make the dict of the items to upgrade and their price
            supply_upgrades[supplies_list[n]] = supply_prices[n]

        # current money/cookie count
        # get the money value
        money = driver.find_element(By.ID, "money").text
        # make money value an integer and replace , in it when there is one
        
        cookie_money = int(money.replace(",", ""))
        # making a dict for possible upgrades
        # makes a list of tuples for the key:value pairs and unpacks them to the temp variables
        for item, cost in supply_upgrades.items():
            # if the total money is grater than the cost
            if cookie_money > cost:
                # add to the possible upgrade dict
                possible_supply_upgrades[item] = cost

        # find the max thing to afford
        # our dict is id:value so can just use this to get the key
        highest_value_item = max(possible_supply_upgrades, key=possible_supply_upgrades.get)

        # buy it
        buy = driver.find_element(By.ID, highest_value_item)
        buy.click()

        check_supplies = time.time() + 5

# when the loop ends this should print out the final cookies/sec
cookies_per_sec = driver.find_element(By.ID, "cps").text
print(f"Reached {cookies_per_sec} clicks per second")