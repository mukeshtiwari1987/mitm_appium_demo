import json
import datetime
import time

CID = "106892"
MID = "99999"
USER_ID = "99999"
JOURNEY_ID = "0"

TRID = CID + "-" + MID + "-" + USER_ID + "-" + JOURNEY_ID + "-"


def generate_trid():
    current_time_object = datetime.datetime.now()
    current_time = current_time_object.strftime("%y" + "%m" + "%d" + "%H" + "%M" + "%S")
    print("current_time: ", current_time)
    trid = TRID + current_time
    return trid


def get_token_from_pn_reg_json():
    print("start of get_token_from_json")
    time.sleep(10)
    with open("pn_register.json", "r") as pn_reg_file:
        json_file_content = json.load(pn_reg_file)
        json_file_content = json.loads(json_file_content)
    user_token = json_file_content['token']
    print("end of get_token_from_json")
    return user_token


def get_pn_deliver_json():
    print("start of get_pn_deliver_json")
    with open("pn_deliver.json", "r") as pn_deliver_file:
        json_file_content = json.load(pn_deliver_file)
        json_file_content = json.loads(json_file_content)
    print("pn_deliver_json content", json_file_content)
    pn_deliver_json = json_file_content
    print("end of get_pn_deliver_json")
    return pn_deliver_json


def get_pn_open_json():
    print("start of get_pn_open_json")
    with open("pn_open.json", "r") as pn_open_file:
        json_file_content = json.load(pn_open_file)
        json_file_content = json.loads(json_file_content)
    print("pn_open_json content", json_file_content)
    pn_open_json = json_file_content
    print("ending get_pn_open_json")
    return pn_open_json
