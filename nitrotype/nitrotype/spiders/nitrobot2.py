import scrapy
#from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
#from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware
import time
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



class NitrobotSpider(scrapy.Spider):
    name = 'nitrobot2'
    allowed_domains = ['www.nitrotype.com']
    start_urls = ['https://www.nitrotype.com/robots.txt']

    def __init__(self):
        self.userList = [
            # {
            #     'username': 'veer1729',
            #     'password': 'Qwerty12@',
            #     'time': 0.06
            # },
            {
                'username': 'windyman101',
                'password': 'owerith43229',
                'time': 0.05
            },
            {
                'username': 'veer1729',
                'password': 'Qwerty12@',
                'time': 0.06
            },
            {
                'username': 'iamslowlyfast',
                'password': 'weiuv3p498',
                'time': 0.08
            }, 
            {
                'username': 'yash_d_love',
                'password': '&zZ2#CS,AAR4A@#',
                'time': 0.05
            },
        ]
        chrome_options = Options()
        # changing the user-agent.
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        chrome_options.add_argument(f"--user-agent={userAgent}")
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_path = which("chromedriver")
        self.driver = webdriver.Chrome(
            executable_path=chrome_path, options=chrome_options)
        self.login(0)

    def login(self, usernumber):
        self.driver.get("https://www.nitrotype.com/login")

        # selenium script to login and render html of the race.

        # check whether already logged in or not.
        # locate the username and password tabs.
        try:
            print("Logging in now")
            user_input = self.driver.find_element_by_xpath(
                "//input[@name='username']")
            password_input = self.driver.find_element_by_xpath(
                "//input[@name='password']")

            # input the values
            user_input.send_keys(self.userList[usernumber]['username'])
            password_input.send_keys(self.userList[usernumber]['password'])
            print("Username and Password typed in!")

            # click on login button.
            login_button = self.driver.find_element_by_xpath(
                "//button[@type='submit']")
            login_button.click()
            print("LOGGED IN!!!")

        except NoSuchElementException:
            print("Already logged in!!!")

        # wait to login
        time.sleep(3)
        # driver.save_screenshot("logged_in.png")

    def logout(self, usernumber):
        try:
            print("Logging out now")
            action = ActionChains(self.driver)
            drop_down = self.driver.find_element_by_link_text(self.userList[usernumber]['username'])
            action.move_to_element(drop_down).perform()
            logout_button = self.driver.find_element_by_link_text("Logout")
            logout_button.click()
            print("LOGGED OUT!!!")

        except NoSuchElementException:
            print("Already logged out!!!")

    def type(self, letter, input_box, usernumber):
        timeToSleep = self.userList[usernumber]['time']
        time.sleep(timeToSleep)
        if letter == "\xa0":
            input_box.send_keys(Keys.SPACE)

        else:
            if letter == "d":
                input_box.send_keys("r")
                time.sleep(timeToSleep)
                input_box.send_keys(letter)

            else:
                input_box.send_keys(letter)
    
    def check_for_recaptcha(self):
        #NOTE NOT GOING TO WORK BECAUSE ITS INSIDE IFRAME AND SCRAPY CANT REACH THERE
        # check for recaptcha.
        #add code for element to be clickable
    
        try:
            print("Switch to the recaptcha frame")
            self.driver.switch_to.frame(self.driver.find_elements_by_xpath("//iframe[contains(@src,'recaptcha')]")[0])
            print("Switch successful!!!")
            recaptcha_checkbox = self.driver.find_element_by_xpath("//span[contains(@class,'recaptcha-checkbox')]")
            print("ReCaptcha Present!!!")
            recaptcha_checkbox.click()
            print("ByPassed ReCaptcha!!!")
            self.driver.switch_to.default_content()
         
        except NoSuchElementException:
            print("ReCaptcha NOT present!!!")
            self.driver.switch_to.default_content()
        
        except IndexError:
            print("Index error")
            print("No such frame found.")

    def parse(self, response):
        print("Reached the parse method")

        # number of times you want to race.
        counter = 800
        usernumber = 0

        for count in range(counter):

            if count % 50 != 49:
                time.sleep(3)

                print("!!!!!!CHECK MARK 1!!!!!")
                self.check_for_recaptcha()

                # go to race.
                self.driver.get("https://www.nitrotype.com/race")

                print("!!!!!!CHECK MARK 2!!!!!")
                self.check_for_recaptcha()

                # wait for race to begin
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@class='dash-copy']"))
                    )
                
                except TimeoutException:
                    flag=True
                    while flag:
                        try:
                            print("TIMEOUT EXCEPTION!!!")
                            print("!!!!!!CHECK MARK 3!!!!!")
                            self.check_for_recaptcha()
                            # go to race.
                            self.driver.get("https://www.nitrotype.com/race")
                            element = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//div[@class='dash-copy']"))
                            )
                            flag=False
                        except TimeoutException:
                            flag=True

                finally:
                    print("The element appeared!!!")

                # wait for 3 secs until the race starts
                time.sleep(4)

                #find input box.
                self.html = self.driver.page_source
                resp = Selector(text=self.html)
                input_box = self.driver.find_element_by_xpath("//input[contains(@class,'dash-copy-input')]")
                isRacing = True

                #skip the first word
                self.type(Keys.ENTER,input_box, usernumber)

                while isRacing:
                    letter1 = resp.xpath("//span[contains(@class, 'is-waiting')]/text()").get()
                    letter2 = resp.xpath("//span[contains(@class, 'is-incorrect')]/text()").get()

                    if letter1 != None:
                        self.type(letter1,input_box,usernumber)

                    elif letter2 != None:
                        self.type(letter2,input_box,usernumber)
                    
                    else:
                        #since either of the letters weren't found, the race must have ended.
                        print("RACE FINISHED!!!")
                        isRacing = False              
                        # wait for results to upload.
                        time.sleep(5)
                    
                    #update the html and response of the page.
                    self.html = self.driver.page_source
                    resp = Selector(text=self.html)

            else:
                #switch to the next user
                self.logout(usernumber)
                time.sleep(5)
                usernumber = (usernumber+1)%5
                self.login(usernumber)
                time.sleep(3)

            yield{"COUNTER":count}

        # close the driver.
        time.sleep(10)
        print("Closing Driver")
        self.driver.close()
        print("Driver Closed")
