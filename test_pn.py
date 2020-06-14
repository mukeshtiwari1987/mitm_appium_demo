import os
import unittest
import pytest

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

carousel_array_value = [{"imgTitle":"Title 1","imgMsg":"Message 1","imgDeeplink":"http://www.netcore.co.in","imgUrl":"https://cdn.pixabay.com/photo/2016/10/27/22/53/heart-1776746_960_720.jpg"},{"imgTitle":"Title 2","imgMsg":"Message 2","imgDeeplink":"profile","imgUrl":"https://cdn.pixabay.com/photo/2018/08/19/19/56/peacock-feathers-3617474_960_720.jpg"},{"imgTitle":"Title 3","imgMsg":"Message 3","imgDeeplink":"smartech://id=5?__sta=%7CUUI&__stm_medium=apn&__stm_source=smartech&__stm_id=133","imgUrl":"https://bellard.org/bpg/2.png"},{"imgTitle":"Title 4","imgMsg":"Message 4","imgDeeplink":"http://www.netcore.co.in","imgUrl":"https://cdn.shopify.com/s/files/1/0257/6087/products/Pikachu_Single_Front_dc998741-c845-43a8-91c9-c1c97bec17a4.png"},{"imgTitle":"Title 5","imgMsg":"Message 5","imgDeeplink":"smartech://id=5?__sta=%7CUUI&__stm_medium=apn&__stm_source=smartech&__stm_id=133","imgUrl":"http://oi67.tinypic.com/1eq3xk.jpg"},{"imgTitle":"Title 6","imgMsg":"Message 6","imgDeeplink":"smartech://id=5?__sta=%7CUUI&__stm_medium=apn&__stm_source=smartech&__stm_id=133","imgUrl":"https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_100kB.jpg"}]

simple_pn_ah = ['', '', 'Simple Android Push Notification AH', 'Redirection AH', [], []]
image_pn_ah = ['https://cdn.pixabay.com/photo/2016/10/27/22/53/heart-1776746_960_720.jpg', '',
               'Image Android Push Notification AH', 'Redirection AH', [], []]
carousel_pn_ah = ['', '', 'Carousel Portrait Push Notification AH', 'Redirection AH', [], carousel_array_value]

PNS = [simple_pn_ah, image_pn_ah,carousel_pn_ah ]


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

    @pytest.mark.parametrize("pn_data", PNS)
    def test_pn_ah(self, pn_data):
        print("start of pn_ah()")

        image_url = pn_data[0]
        deeplink_content = pn_data[1]
        title_content = pn_data[2]
        message_content = pn_data[3]
        action_button_content = pn_data[4]
        carousel_content = pn_data[5]
        trid = generate_trid()

        print("start of fcm")
        fcm_response = fcm_request.execute_rest_api(self.user_token,
                                                    image=image_url,
                                                    deep_link=deeplink_content,
                                                    title=title_content,
                                                    message=message_content,
                                                    action_button=action_button_content,
                                                    carousel=carousel_content,
                                                    trid=trid)
        print(fcm_response)
        print("end of fcm")

        self.driver.open_notifications()
        notification_items = self.driver.find_elements_by_id("android:id/title")
        print(f'number of notifications: {len(notification_items)}')

        wait = WebDriverWait(self.driver, 30, 10)

        try:
            title_on_device = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//android.widget.TextView[contains(@text, '" + title_content + "')]")))
            assert title_on_device.text == title_content

            if title_on_device.text:
                pn_deliver_json = get_pn_deliver_json()
                assert pn_deliver_json["trid"] == trid
                print("pn_deliver_json trid assertion success. trid: ", pn_deliver_json["trid"])
                assert pn_deliver_json["action"] == "delivered"
                print("pn_deliver_json action assertion success. trid: ", pn_deliver_json["action"])
                assert pn_deliver_json["eventid"] == "12"
                print("pn_deliver_json eventid assertion success. trid: ", pn_deliver_json["eventid"])

                print("click notification")
                title_on_device.click()

                pn_open_json = get_pn_open_json()
                assert pn_open_json["trid"] == trid
                print("pn_open_json trid assertion success. trid: ", pn_open_json["trid"])
                assert pn_open_json["action"] == "open"
                print("pn_open_json action assertion success. trid: ", pn_open_json["action"])
                assert pn_open_json["eventid"] == "13"
                print("pn_open_json eventid assertion success. trid: ", pn_open_json["eventid"])

        except TimeoutException:
            print("Could not find simple_pn_ah_title")

        print("end of pn_ah()")


if __name__ == '__main__':
    # run test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPN)
    unittest.TextTestRunner(verbosity=2).run(suite)
