from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

chrome_path="E:/All in/Final Year Project/Akki/Programmes/chromedriver_win32/chromedriver.exe"
chrome_options = Options()
chrome_options.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 2})
desired_cap = chrome_options.to_capabilities()
desired_cap.update({
    'browser_version': '75.0',
    'os': 'Windows',
    'os_version': '10'
})
driver = webdriver.Chrome(executable_path=chrome_path,desired_capabilities=desired_cap)

driver.get('https://www.facebook.com/teajarsl/photos/a.257902255604239/258287885565676/?type=3&theater')
# time.sleep(10)
print("Opened facebook...")
email = driver.find_element_by_xpath("//input[@id='email' or @name='email']")
email.send_keys('milanda.wijekoon1@gmail.com')
print("email entered...")
password = driver.find_element_by_xpath("//input[@id='pass']")
password.send_keys('1996723pavi')
print("Password entered...")
button = driver.find_element_by_xpath("//*[@id='u_0_2']")
button.click()
print("facebook opened")

time.sleep(10)
# comment = driver.find_element_by_xpath('//*[@id="u_3_2"]/div[2]/div/div[2]/div[2]/span[2]/a').click()

# for i in range(1,11):
comment = driver.find_element_by_xpath("//*[@id='fbPhotoSnowliftFeedbackInput']/div/div/div[2]/div/div/div/div/div/form/div/div/div/div/div/div/div/span")
comment.send_keys(u'\u1600')
time.sleep(5)
comment.send_keys(Keys.ENTER)





