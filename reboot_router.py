import os.path
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""
This scripts reboots your router using selenium web driver. 
This script was written for tplink archer c5 router
"""
file_path = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser()
config_file_path = os.path.join(file_path, 'pass.ini') if os.path.exists(
    os.path.join(file_path, 'pass.ini')) else os.path.join(file_path, 'pass_git.ini')
config.read(config_file_path)
chrome_options = Options()
chrome_options.add_argument("--headless")


def main():
    driver = webdriver.Chrome(config.get('SETTINGS', 'chrome_driver'), options=chrome_options)
    driver.get(config.get('SETTINGS', 'router_url'))
    driver.find_element('id', 'pc-login-password').send_keys(config.get('SETTINGS', 'password'))
    driver.find_element('id', 'pc-login-btn').click()
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'topReboot')))
        element.click()
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//span[.='Yes']")))
        element.click()
    finally:
        driver.quit()
