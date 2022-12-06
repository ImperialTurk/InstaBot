from instaUserInfo import username,password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Instagram:
    def __init__(self, username, password):
        self.browserProfie = webdriver.ChromeOptions()
        self.browserProfie.add_experimental_option("prefs", {"intl.accept_languages":"en,en_US"})
        self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=self.browserProfie)
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(3)
        userInput = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        passInput = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')

        userInput.send_keys(self.username)
        passInput.send_keys(self.password)
        passInput.send_keys(Keys.ENTER)
        time.sleep(5)

    def getFollowers(self, max):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)

        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followerCount = len(dialog.find_elements_by_css_selector("li"))
        
        print(f"first count: {followerCount}")

        action = webdriver.ActionChains(self.browser)

        while followerCount < max:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)
            newCount = len(dialog.find_elements_by_css_selector("li"))
            
            if followerCount != newCount:
                followerCount = newCount
                print(f"second count: {newCount}")
                time.sleep(1)
            else:
                break

        followers = dialog.find_elements_by_css_selector("li")

        followersList = []
        i = 0
        for user in followers:
            i += 1
            if i == max:
                break
            link = user.find_element_by_css_selector("a").get_attribute("href")
            followersList.append(link)
        
        with open("followers.txt", "w", encoding="UTF-8") as file:
            for item in followersList:
                file.write(item + "\n")

    def followUser(self, username):
        self.browser.get("https://www.instagram.com/"+username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name("button")
        if followButton.text != "Message":
            followButton.click()
            time.sleep(2)
        else:
            print("Zaten takiptesin")

    def unFollowUser(self,username):
        self.browser.get("https://www.instagram.com/"+username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        if followButton.text == "Message":
            unfollow = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
            time.sleep(2)
            unfollow.click()
            self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
        else:
            print("Zaten takip etmiyorsunuz")


instagram = Instagram(username, password)
instagram.signIn()
#instagram.getFollowers(50)
#instagram.followUser("kod_evreni")

# liste = [" ", " ", " "]
# for user in liste:
#     instagram.followUser(user)

#instagram.unFollowUser("kod_evreni")