from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import youtube_uploader_selenium
from typing import  Optional
import pickle
from .const import Constant as Const
from os import path,mkdir
import tldextract
from pathlib import Path



class ViralPulse:
    """
        A great tool to upload videos to different platforms
    """
    def __init__(self,video_path,metadata: Optional[str] = None , cookies_folder_path : Optional[str] = "cookies") -> None:
        self.driver = webdriver.Firefox()
        self.cookies_folder_path =  Path.cwd().joinpath(cookies_folder_path)
        self.video_path = str(Path.cwd().joinpath(video_path).absolute().resolve())

    def youtube_uploader(self):
        try:
            self.__login()
            sleep(2)
            self.__upload()
        except Exception as error:
            print(error)
            self.__quit()

    def __login(self):
        self.driver.get(Const.YOUTUBE_URL)
        sleep(2)

        if self.has_cookies_for_current_url():
            self.__load_cookies()
            sleep(2)
            self.driver.refresh()
        else:
            print("Please Login then press any key to continue ...") 
            input()
            self.__save_cookies()


    def __upload(self):
        self.driver.get(Const.YOUTUBE_URL)
        sleep(6)
        self.driver.get(Const.YT_UPLOAD_URL)
        sleep(8)
        video_abs_path = self.video_path
        self.driver.find_element_by_xpath(Const.VIDEO_INPUT).send_keys(video_abs_path)
        sleep(6)
        self.driver.find_element_by_id(Const.TITLE_SELECTOR).click()

        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_down(Keys.DELETE).key_up(Keys.DELETE).send_keys("simple title").perform()
        sleep(3)


        self.driver.find_element_by_id(Const.DESCRIPTION_SELECTOR).click()
        sleep(3)
        ActionChains(self.driver).send_keys("simple description").perform()
        sleep(3)

        self.driver.find_element_by_name(Const.NOT_KIDS_SELECTOR).click()
        sleep(3)

        self.driver.find_element_by_css_selector(Const.NEXT_BUTTON2).click()
        sleep(6)
        self.driver.find_element_by_css_selector(Const.NEXT_BUTTON2).click()
        sleep(6)
        self.driver.find_element_by_css_selector(Const.NEXT_BUTTON2).click()
        sleep(3)
        self.driver.find_element_by_name(Const.VISIBILITY_SELECTOR).click()
        sleep(6)
        self.driver.find_element_by_css_selector(Const.PUBLISH_BUTTON).click()
     

    def __load_cookies(self):
        cookies = pickle.load(open(self.__cookies_path(), "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
    def __save_cookies(self):
        pickle.dump(self.driver.get_cookies(), open(self.__cookies_path(), "wb"))


    def has_cookies_for_current_url(self) -> bool:
        if not path.exists(self.cookies_folder_path):
            mkdir(self.cookies_folder_path)
        return path.exists(self.__cookies_path())

    
    def __cookies_path(self):
        url_comps = tldextract.extract(self.driver.current_url)
        formatted_url = url_comps.domain + '.' + url_comps.suffix

        return path.join(
            self.cookies_folder_path,
            formatted_url + '.pkl'
        )
    def __quit(self):
        self.driver.quit()


    
