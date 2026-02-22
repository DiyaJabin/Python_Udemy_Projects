from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver,3)

    def login(self, url, username, password):
        self.driver.get(url)
        self.driver.maximize_window()
        username_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='email']")))
        username_input.send_keys(username)
        password_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='pass']")))
        password_input.send_keys(password)

        login_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                         "//div[@class='x1i10hfl xjbqb8w x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x1ypdohk x3ct3a4 xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x16tdsg8 x1hl2dhg xggy1nq x1fmog5m xu25z0z x140muxe xo1y3bh x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3']")))
        login_button.click()

        try:
            dont_save_login_info = self.short_wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='x1i10hfl xjqpnuy xc5r6h4 xqeqjp1 x1phubyo xdl72j9 x2lah0s x3ct3a4 xdj266r x14z9mp xat24cr x1lziwak x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1a2a7pz x6s0dn4 xjyslct x1ejq31n x18oe1m7 x1sy0etr xstzfhl x9f619 x1ypdohk x1f6kntn xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc x5c86q x18br7mf x1i0vuye xl0gqc1 xr5sc7 xlal1re x14jxsvd xt0b8zv xjbqb8w xr9e8f9 x1e4oeot x1ui04y5 x6en5u8 x972fbf x10w94by x1qhh985 x14e42zd xt0psk2 xt7dq6l xexx8yu xyri2b x18d9i69 x1c1uobl x1n2onr6 x1n5bzlp']")))
            dont_save_login_info.click()
        except NoSuchElementException,TimeoutException:
            pass

        try:
            continue_button = self.short_wait.until(EC.visibility_of_element_located((By.XPATH,
                                                    "//div[@class='x1ja2u2z x78zum5 x2lah0s x1n2onr6 xl56j7k x6s0dn4 xozqiw3 x1q0g3np x972fbf x10w94by x1qhh985 x14e42zd x9f619 xtvsq51 xqbgfmv xbe3n85 x7a1id4 x1d9i5bo x1xila8y x1bumbmr xc8cyl1']")))
            continue_button.click()
        except NoSuchElementException,TimeoutException:
            pass
        try:
            password_entry = self.short_wait.until(EC.presence_of_element_located((By.XPATH,"//input[@type='password']")))
            password_entry.send_keys(password)
            login_button = self.short_wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='x1ey2m1c xtijo5x x1o0tod xg01cxk x47corl x10l6tqk x13vifvy x1ebt8du x19991ni x1dhq9h x1fmog5m xu25z0z x140muxe xo1y3bh']")))
            login_button.click()
        except NoSuchElementException,TimeoutException:
            pass
    def find_followers(self, account_name):
        self.driver.get(f"https://www.instagram.com/{account_name}/")
        view_followers = self.wait.until(EC.presence_of_element_located((By.XPATH,f'//a[@href="/{account_name}/followers/"]')))
        view_followers.click()

        follower_popup = self.wait.until(EC.presence_of_element_located((By.XPATH,"//div[@role='dialog']")))

        last_height = 0

        while True: #Keep scrolling until no new followers load
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", follower_popup) #Scroll the popup to the bottom
            time.sleep(2) #Wait for 2s to let new followers load
            try:
                new_height = self.driver.execute_script("return arguments[0].scrollHeight;", follower_popup) #Get to total scrollable height after scrolling
            except StaleElementReferenceException:
                #re-find popup and try
                follower_popup=self.wait.until(EC.presence_of_element_located((By.XPATH,"//div[@role='dialog']")))
                new_height = self.driver.execute_script("return arguments[0].scrollHeight;", follower_popup)
            '''Explanation:
            execute_script() lets Selenium run Javascript inside the browser, the arguments passed on after 
            that piece of code are Javascript arguments. argument[0] is the first argument passed from 
            Selenium into this script, which is follower_popup.
            scrollTop : how far you have scrolled from the top(in pixels)
            scrollHeight: total height of the contents inside that element 
            
            arguments[0].scrollTop = arguments[0].scrollHeight translates to:
            current scroll position = total content height, hence there is instant scrolling to the bottom.'''

            if new_height == last_height: #If height didn't increase, no new followers were loaded
                break

            last_height = new_height



    def follow(self):
        pass
