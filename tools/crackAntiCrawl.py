from selenium import webdriver
import os


cur_path = os.path.dirname(os.path.abspath(__file__))
gecko_path = os.path.join(cur_path, 'geckodriver')


class CrackAntiCrawl(object):
    def __init__(self):
        self.cookie_66ip = None

    def crack_66ip(self):
        if self.cookie_66ip:
            return self.cookie_66ip
        geckodriver = gecko_path

        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        browser = webdriver.Firefox(executable_path=geckodriver, firefox_options=options)

        browser.get('http://www.66ip.cn')
        cookie_list = browser.get_cookies()
        cookies = {}
        for i in cookie_list:
            cookies[i['name']] = i['value']
        browser.quit()
        self.cookie_66ip = cookies
        return cookies

