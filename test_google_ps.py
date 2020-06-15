import os
import unittest
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from appium import webdriver

APK_LOCATION = '/home/mukesh.tiwari/Downloads/nativeapps/' \
               '2020-05-26-bkram_test_a43fb6fc9f588f00c18a2e931c53a61c-2.5.1_without_xiaomi.apk'


class TestGooglePS:
    def setup_class(self):
        desired_caps = {'platformName': 'Android',
                        'platformVersion': '8.1.0',
                        'deviceName': 'emulator-5554',
                        'automationName': 'UiAutomator2',
                        'fullReset': 'false',
                        'eventTimings': 'true',
                        'adbExecTimeout': '50000',
                        'autoGrantPermissions': 'true',
                        'appPackage': 'com.android.vending',
                        'appActivity': 'com.google.android.finsky.activities.MainActivity'}

        print("Executing webdriver.Remote()")
        self.driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)

    def teardown_class(self):
        print("Executing driver.quit()")
        self.driver.quit()

    def teardown_method(self):
        print("start of teardown_method")
        self.driver.save_screenshot("proof.png")
        self.clear_pn()
        self.driver.press_keycode(3)
        print("end of teardown_method")

    def clear_pn(self):
        try:
            self.driver.swipe(400, 400, 0, 300)
            # driver.find_element_by_id("com.android.systemui:id/dismiss_text").click()
        except NoSuchElementException:
            print("Clear All Button not found")

    def test_google_pn(self):
        print("test_google_pn")

        wait = WebDriverWait(self.driver, 60, 10)
        try:
            play_store_search_bar_hint = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//android.widget.TextView[contains(@text, 'Search for apps & games')]")))
            assert play_store_search_bar_hint.text == 'Search for apps & games'
            play_store_search_bar_hint.click()

            search_bar_text_input = self.driver.find_element_by_id("com.android.vending:id/search_bar_text_input")
            assert search_bar_text_input .text == 'Search for apps & games'
            search_bar_text_input.send_keys("makemytrip")
        except TimeoutException:
            print("Could not find Search for apps & games")

        try:
            app_in_search_list = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//android.widget.TextView[contains(@text,'makemytrip-flights hot')]")))
            app_in_search_list.click()
        except TimeoutException:
            print("Could not find makemytrip-flights hot")

        try:
            app_domain_icon = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//android.widget.FrameLayout[contains(@content-desc,"
                          "'MakeMyTrip-Flight Hotel Bus Cab IRCTC')]")))
            app_domain_icon.click()
        except TimeoutException:
            print("Could not find MakeMyTrip-Flight Hotel Bus Cab IRCTC")

        try:
            install_button = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//android.widget.Button[contains(@text, 'Install')]")))
            assert install_button.text == "Install"
            install_button.click()
        except TimeoutException:
            print("Could not find Install button")

        try:
            wait = WebDriverWait(self.driver, 240, 30)
            open_button = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//android.widget.Button[contains(@text, 'Open')]")))
            assert open_button.text == "Open"
            open_button.click()
        except TimeoutException:
            print("Could not find Open button")
