import os
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from appium import webdriver

from utils.json_read_write import generate_trid, get_token_from_pn_reg_json, get_pn_deliver_json, get_pn_open_json
import fcm_request

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

APK_LOCATION = '/home/mukesh.tiwari/Downloads/nativeapps/' \
               '2020-05-26-bkram_test_a43fb6fc9f588f00c18a2e931c53a61c-2.5.1_without_xiaomi.apk'


class TestPN:

    def setup_class(self):
        desired_caps = {'platformName': 'Android',
                        'platformVersion': '8.1.0',
                        'deviceName': 'emulator-5554',
                        'automationName': 'UiAutomator2',
                        'fullReset': 'false',
                        'eventTimings': 'true',
                        'adbExecTimeout': '50000',
                        'autoGrantPermissions': 'true',
                        'app': APK_LOCATION}

        print("Executing webdriver.Remote()")
        self.driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, "skipTextView")))
        self.user_token = get_token_from_pn_reg_json()

        self.simple_pn_ah_title = "Simple Android Push Notification AH"
        self.pn_ah_message_text = "Redirection AH"

    def teardown_class(self):
        print("Executing driver.quit()")
        self.driver.quit()

    def setup_method(self):
        print("token :", self.user_token)
        self.trid = generate_trid()
        print("trid :", self.trid)

        fcm_response = fcm_request.execute_rest_api(self.user_token,
                                                    image="",
                                                    deep_link="",
                                                    title=self.simple_pn_ah_title,
                                                    message=self.pn_ah_message_text,
                                                    action_button=[],
                                                    carousel=[],
                                                    trid=self.trid)

        print(fcm_response)

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

    def test_simple_pn_ah(self):
        print("start of simple_pn_ah()")
        self.driver.open_notifications()
        notification_items = self.driver.find_elements_by_id("android:id/title")
        print(f'number of notifications: {len(notification_items)}')

        wait = WebDriverWait(self.driver, 30, 10)

        try:
            simple_pn_ah_title_on_device = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//android.widget.TextView[contains(@text, 'Simple Android Push Notification AH')]")))
            assert simple_pn_ah_title_on_device.text == self.simple_pn_ah_title

            if simple_pn_ah_title_on_device.text:
                pn_deliver_json = get_pn_deliver_json()
                assert self.trid == pn_deliver_json["trid"]
                print("pn_deliver_json trid assertion success. trid: ", pn_deliver_json["trid"])
                assert pn_deliver_json["action"] == "delivered"
                print("pn_deliver_json action assertion success. trid: ", pn_deliver_json["action"])
                assert pn_deliver_json["eventid"] == "12"
                print("pn_deliver_json eventid assertion success. trid: ", pn_deliver_json["eventid"])

                print("click notification")
                simple_pn_ah_title_on_device.click()

                pn_open_json = get_pn_open_json()
                assert pn_open_json["trid"] == self.trid
                print("pn_open_json trid assertion success. trid: ", pn_open_json["trid"])
                assert pn_open_json["action"] == "open"
                print("pn_open_json action assertion success. trid: ", pn_open_json["action"])
                assert pn_open_json["eventid"] == "13"
                print("pn_open_json eventid assertion success. trid: ", pn_open_json["eventid"])

        except TimeoutException:
            print("Could not find simple_pn_ah_title")

        print("end of simple_pn_ah()")


if __name__ == '__main__':
    # run test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPN)
    unittest.TextTestRunner(verbosity=2).run(suite)
