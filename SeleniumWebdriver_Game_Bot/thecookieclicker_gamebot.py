from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")
driver.maximize_window()
time.sleep(2)


cookie_acceptance = driver.find_element(By.XPATH,"//a[@class = 'cc_btn cc_btn_accept_all']")
cookie_acceptance.click()

time.sleep(2)
language_select=driver.find_element(By.XPATH,"//div[@id='langSelect-EN']")
language_select.click()

time.sleep(2)
cookie_acceptance_2 = driver.find_element(By.XPATH,"//a[@data-cc-event = 'click:dismiss']")
cookie_acceptance_2.click()

game_on = True
while game_on:
    end_time= time.time()+5
    cookie = driver.find_element(By.XPATH, "//button[@ id = 'bigCookie']")
    while time.time()<end_time:
        cookie.click()
    time.sleep(2)
    try:
        close_sidenotes = driver.find_element(By.XPATH,"//div[@class = 'framed close sidenote']")
        close_sidenotes.click()
    except NoSuchElementException:
        pass
    time.sleep(1)
    for product_id in ["product3","product2","product1","product0"]: #Give priority to the costliest one firstt
        try:
            update_skill = driver.find_element(By.XPATH,f"//div[@id = '{product_id}']")
            if "enabled" in update_skill.get_attribute("class"):
                update_skill.click()
        except NoSuchElementException:
            pass
    time.sleep(1)





