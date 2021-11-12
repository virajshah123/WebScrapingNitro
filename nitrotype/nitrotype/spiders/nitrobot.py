import scrapy
#from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
#from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware
#from selenium.webdriver.common.keys import Keys
import time
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#import pyautogui

class NitrobotSpider(scrapy.Spider):
    name = 'nitrobot'
    allowed_domains = ['www.nitrotype.com']
    start_urls = ['https://www.nitrotype.com/robots.txt']
    #handle_httpstatus_list = [403]
    #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

    def login(self):
        self.driver.get("https://www.nitrotype.com/login")
        
        #selenium script to login and render html of the race.
        username = "Yash_D_love"
        password = "&zZ2#CS,AAR4A@#"

        #check whether already logged in or not.
        #locate the username and password tabs.
        try:
            print("Logging in now")
            user_input = self.driver.find_element_by_xpath("//input[@name='username']")
            password_input = self.driver.find_element_by_xpath("//input[@name='password']")

            #input the values
            user_input.send_keys(username)
            password_input.send_keys(password)
            print("Username and Password typed in!")
            
            #click on login button.
            login_button = self.driver.find_element_by_xpath("//button[@type='submit']")
            login_button.click()
            print("LOGGED IN!!!")

        except NoSuchElementException:
            print("Already logged in!!!")
        
        #wait to login
        time.sleep(3)
        #driver.save_screenshot("logged_in.png")

    
    def logout(self):
        try:
            print("Logging out now")
            action = ActionChains(self.driver)
            drop_down = self.driver.find_element_by_link_text("yash_d_love")
            action.move_to_element(drop_down).perform()
            logout_button = self.driver.find_element_by_link_text("Logout")
            logout_button.click()
            print("LOGGED OUT!!!")

        except NoSuchElementException:
            print("Already logged out!!!")

    
    def __init__(self):
        chrome_options = Options()
        #changing the user-agent.
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        chrome_options.add_argument(f"--user-agent={userAgent}")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_path = which("chromedriver")
        self.driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        self.login()
          
        

    def parse(self, response):
        print("Reached the parse method")

        #number of times you want to race.
        counter = 20

        for count in range(counter):

            if count%5 != 1:
                #go to race.
                self.driver.get("https://www.nitrotype.com/race")
                
                #wait for race to begin
                try:
                    element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='dash-copy']"))
                    )
                finally:
                    print("The element appeared!!!")
            
                #self.driver.save_screenshot("race.png")

                self.html = self.driver.page_source
                
                #wait for 3 secs until the race starts
                time.sleep(5)
                resp = Selector(text=self.html)
                box = resp.xpath("//div[@class='dash-copy']")
                words = box.xpath(".//span[@class='dash-word']")
                input_box = self.driver.find_element_by_xpath("//input[@class='dash-copy-input']")

                #extract the words for the race.
                for word in words:
                    letters = word.xpath(".//span[contains(@class,'dash-letter')]/text()").getall()
                    yield {'word': letters}

                    #type the words, extract from the words.json file.
                    for letter in letters:
                        time.sleep(0.1)
                        if letter == "\xa0":
                            input_box.send_keys(Keys.SPACE)
                            #pyautogui.write(" ")
                                
                        else:
                            if letter == "t" or letter == "e":
                                input_box.send_keys("r")
                                time.sleep(0.1)
                                input_box.send_keys(letter)
                                    
                            else:
                                input_box.send_keys(letter)
                                #pyautogui.write(letter)
                                

                #wait for results to upload.
                time.sleep(5)

            else:
                #logout, wait and then login.
                self.logout()
                time.sleep(10)
                self.login()
        
        time.sleep(10)

        #close the driver.
        print("Closing Driver")
        self.driver.close()
        print("Driver Closed")
    