import time
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from appium import webdriver

from utils.json_read_write import get_token_from_pn_reg_json, get_pn_deliver_json, generate_trid
import fcm_request


user_token = "None"

APK_LOCATION = '/home/mukesh.tiwari/Downloads/nativeapps/' \
               '2020-05-26-bkram_test_a43fb6fc9f588f00c18a2e931c53a61c-2.5.1_without_xiaomi.apk'

SHORT_WAIT = 5
MEDIUM_WAIT = 15
LONG_WAIT = 30

desired_caps = {'platformName': 'Android',
                'platformVersion': '8.1.0',
                'deviceName': 'emulator-5554',
                'automationName': 'UiAutomator2',
                'fullReset': 'false',
                'eventTimings': 'true',
                'adbExecTimeout': '50000',
                'autoGrantPermissions': 'true',
                'app': APK_LOCATION}

print("starting appium driver")
driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)
driver.implicitly_wait(5)

pn_ah_message_text = "Redirection AH"


# def get_token_from_ui():
#     print("starting get_token()")
#     driver.find_element_by_id("skipTextView").click()
#     driver.find_element_by_xpath("//android.widget.TextView[contains(@text, 'Settings')]").click()
#     driver.find_element_by_xpath("//android.widget.TextView[contains(@text, 'Smartech Preferences')]").click()
#     global user_token
#     user_token = driver.find_element_by_id("tv_value").text
#     print(user_token)
#     driver.press_keycode(3)
#     time.sleep(5)
#     print("ending get_token()")


def clear_pn():
    try:
        driver.swipe(400,400,0,300)
        # driver.find_element_by_id("com.android.systemui:id/dismiss_text").click()
    except NoSuchElementException:
        print("Clear All Button not found")


def simple_pn_ah():
    print("starting simple_pn_ah()")

    simple_pn_ah_title = "Simple Android Push Notification AH"
    WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.ID, "skipTextView")))
    time.sleep(MEDIUM_WAIT)

    print("before get token from json in simple pn ah")
    global user_token
    user_token = get_token_from_pn_reg_json()
    print("after get token from json in simple pn ah")
    trid = generate_trid()
    print("trid :", trid)

    fcm_response = fcm_request.execute_rest_api(user_token,
                                                image="",
                                                deep_link="",
                                                title=simple_pn_ah_title,
                                                message=pn_ah_message_text,
                                                action_button=[],
                                                carousel=[],
                                                trid=trid)

    print(fcm_response)
    driver.open_notifications()
    notification_items = driver.find_elements_by_id("android:id/title")
    print(f'number of notifications: {len(notification_items)}')

    wait = WebDriverWait(driver, 30, 10)
    try:
        simple_pn_ah_title_on_device = wait.until(ec.visibility_of_element_located((
            By.XPATH, "//android.widget.TextView[contains(@text, 'Simple Android Push Notification AH')]")))
        assert simple_pn_ah_title_on_device.text == simple_pn_ah_title
    except TimeoutException:
        print("Could not find simple_pn_ah_title")

    try:
        if simple_pn_ah_title_on_device.text == simple_pn_ah_title:
            pn_deliver_json = get_pn_deliver_json()
            print("pn_deliver_json in simple_pn_ah()", pn_deliver_json)
            assert trid == pn_deliver_json["trid"]
    except UnboundLocalError:
        print("Could not find simple_pn_ah_title_on_device.text")

    # driver.get_system_bars()
    # sb = driver.find_elements_by_android_uiautomator('new UiSelector().text("status_bar_latest_event_content")')
    # print(type(sb))
    # print(dir(sb))
    # com.android.systemui: id / expanded)

    driver.save_screenshot("simple_pn_ah_before_pn_click.png")
    clear_pn()
    driver.press_keycode(3)
    print("ending simple_pn_ah()")


# def image_pn_ah():
#     print("starting image_pn_ah()")
#
#     image_pn_ah_title = "Image Android Push Notification AH"
#
#     fcm_response = fcm_request.execute_rest_api(user_token,
#                                                 image="https://cdn.pixabay.com/photo/2016/10/27/22/53/heart-1776746_960_720.jpg",
#                                                 deep_link="",
#                                                 title=image_pn_ah_title,
#                                                 message=pn_ah_message_text,
#                                                 action_button=[],
#                                                 carousel=[])
#
#     print(fcm_response)
#     driver.open_notifications()
#     notification_items = driver.find_elements_by_id("android:id/title")
#     print(f'number of notifications: {len(notification_items)}')
#
#     wait = WebDriverWait(driver, 10, 5)
#     image_pn_ah_title = wait.until(ec.visibility_of_element_located((
#         By.XPATH, "//android.widget.TextView[contains(@text, 'Image Android Push Notification AH')]")))
#
#     driver.save_screenshot("/home/mukesh.tiwari/Documents/shastra/ncore_app/paf/image_pn_ah_before_pn_click.png")
#     clear_pn()
#     driver.press_keycode(3)
#     print("ending image_pn_ah()")

if __name__ == '__main__':
    # get_token_from_ui()
    # global user_token
    simple_pn_ah()
    # image_pn_ah()
    driver.quit()
