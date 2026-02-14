from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
load_dotenv()

#-------CONSTANTS--------
YOUR_EMAIL = os.getenv("MY_EMAIL")
YOUR_PASSWORD = os.getenv("MY_PASSWORD")
CLASSES_BOOKED = 0
WAITLISTS_JOINED = 0
ALREADY_BOOKED_WAITLISTED = 0
TOTAL_6PM_CLASS_PROCESSED_TUE_SAT = 0
TOTAL_BOOKINGS_WAITLISTS=0
GYM_URL = "https://appbrewery.github.io/gym/"

#------MAIN_CODE-----------
chrome_options = webdriver.ChromeOptions() #Create configuration object
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile") #Create a directory to store chrome profile information
#os.getcwd gives the current working directory, join joins these paths to give the path of the user profile
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
#Complete the chrome options, then make the driver object

driver = webdriver.Chrome(options = chrome_options)
wait = WebDriverWait(driver,15)

driver.get(GYM_URL)
driver.maximize_window()


login_button = wait.until(EC.visibility_of_element_located((By.XPATH,"//button[@id='login-button']")))
login_button.click()

email_input = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@id='email-input']")))
email_input.send_keys(f"{YOUR_EMAIL}")

password_input = driver.find_element(By.XPATH,"//input[@id='password-input']")
password_input.send_keys(f"{YOUR_PASSWORD}")

submit_credentials_button = driver.find_element(By.XPATH,"//button[@id='submit-button']")
submit_credentials_button.click()

newly_processed_classes = []
proceed = False

possible_class_buttons = wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//button[contains(@id,'1800')]")))
for possible_class in possible_class_buttons:
    parent_div = possible_class.find_element(By.XPATH,"ancestor::div[contains(@class,'Schedule_dayGroup')]")
    what_day = parent_div.find_element(By.XPATH,".//h2[contains(@class,'Schedule_dayTitle')]")
    if "(" not in what_day.text:
        if what_day.text.split(",")[0] in ("Tue","Sat"):
            proceed = True
        else:
            proceed = False
    else :
        if what_day.text.split("(")[1].split(",")[0] in ("Tue","Sat"):
            proceed = True
        else:
            proceed = False
    if proceed:
        TOTAL_6PM_CLASS_PROCESSED_TUE_SAT+=1
        button_id = possible_class.get_attribute("id")
        token = button_id.replace("book-button-","")
        class_type = driver.find_element(By.ID,f"class-name-{token}") #Since button and class type have very similar IDs, can be used to locate the button
        if possible_class.text =="Book Class":
            wait.until(EC.element_to_be_clickable(possible_class)).click()
            print(f" ✔ Successfully Booked !! : {class_type.text} on {what_day.text}")
            newly_processed_classes.append(f"[New Booking] {class_type.text} on {what_day.text}")
            CLASSES_BOOKED+=1
        elif possible_class.text == "Waitlisted":
            print(f" ✔ Already on the waitlist: {class_type.text} on {what_day.text}")
            ALREADY_BOOKED_WAITLISTED+=1
        elif possible_class.text =="Booked":
            print(f" ✔ Already booked! : {class_type.text} on {what_day.text}")
            ALREADY_BOOKED_WAITLISTED+=1
        elif possible_class.text =="Join Waitlist":
            wait.until(EC.element_to_be_clickable(possible_class)).click()
            print(f" ✔ Joined waitlist for: {class_type.text} on {what_day.text}")
            newly_processed_classes.append(f"[New Waitlist] {class_type.text} on {what_day.text}")
            WAITLISTS_JOINED+=1

TOTAL_BOOKINGS_WAITLISTS=ALREADY_BOOKED_WAITLISTED+CLASSES_BOOKED+WAITLISTS_JOINED

#------OUTPUT PRINTING-----
print("--------BOOKING STATUS--------")
print(f"Classes booked: {CLASSES_BOOKED}")
print(f"Waitlists joined: {WAITLISTS_JOINED}")
print(f"Already booked/waitlisted: {ALREADY_BOOKED_WAITLISTED}")
print(f"Total Tuesday and Saturday 6pm classes processed: {TOTAL_6PM_CLASS_PROCESSED_TUE_SAT}")

if newly_processed_classes:
    print("\n\n----DETAILED CLASS LIST----")
    for i in newly_processed_classes:
        print(f"• {i}")

#-------VERIFICATION-------
print("\n\n-----VERIFYING ON MY BOOKINGS PAGE-----")
time.sleep(2)
verified_classes=[]
my_bookings_link = wait.until(EC.visibility_of_element_located((By.XPATH,"//a[@id='my-bookings-link']")))
my_bookings_link.click()
try:
    confirmed_bookings_div = driver.find_element(By.XPATH,"//div[@id='confirmed-bookings-section']")
    confirmed_bookings=confirmed_bookings_div.find_elements(By.XPATH,".//h3[contains(@id,'booking-class-name')]")
    for i in confirmed_bookings:
        verified_classes.append(i.text)
except NoSuchElementException:
    pass
try:
    confirmed_waitlists_div = driver.find_element(By.XPATH,"//div[@id='waitlist-section']")
    confirmed_waitlists=confirmed_waitlists_div.find_elements(By.XPATH,".//h3[contains(@id,'waitlist-class-name')]")
    for i in confirmed_waitlists:
        verified_classes.append(i.text)
except NoSuchElementException:
    pass

if verified_classes:
    for i in verified_classes:
        print(f"✔ Verified: {i}")
else:
    print("No classes booked/waitlists joined")

print("\n\n------VERIFICATION RESULT-----")
print(f"Expected: {TOTAL_BOOKINGS_WAITLISTS}")
print(f"Found: {len(verified_classes)}")
if len(verified_classes) == TOTAL_BOOKINGS_WAITLISTS:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: {TOTAL_BOOKINGS_WAITLISTS-len(verified_classes)}")


