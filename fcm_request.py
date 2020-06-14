import requests
import json
import time
import datetime


FCM_URL = "https://fcm.googleapis.com/fcm/send"
FCM_KEY = "key=AAAAtJTBAjA:APA91bFArxep1J1qTLku6qDOCmZjq4a2P-HX1_tAOe8KRG0Wd_OS8mRNXxGc8YUv79dssY0ERGToO-1XkbYPOp7teafUkniRd0t8W3fp97yuiJeepMzrWB5MxnWuVUUg611-67Y7fUXP"
MY_TOKEN = "dummy_token"

# CID = "106892"
# MID = "99999"
# USER_ID = "99999"
# JOURNEY_ID = "0"
#
# TRID = CID + "-" + MID + "-" + USER_ID + "-" + JOURNEY_ID


def execute_rest_api(user_token,
                     image="",
                     deep_link="",
                     title=None,
                     message=None,
                     action_button=[],
                     carousel=[],
                     trid=None):

    # epoch_time = str(time.time())
    #
    # print("epoch time", epoch_time)

    # 200526135052

    # current_time_object = datetime.datetime.now()
    # print("current_time_object: ", current_time_object)
    # current_time = current_time_object.strftime("%y" + "%m" + "%d" + "%H" + "%M" + "%S")
    # print("current_time: ",current_time)

    headers = {
        'Authorization': FCM_KEY,
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "fcm.googleapis.com",
        'accept-encoding': "gzip, deflate",
        'content-length': "560",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    payload = {
        "to": user_token,
        "data": {
            "data": {
                "image": image,
                "sound": True,
                "deeplink": deep_link,
                "actionButton": action_button,
                "expiry": 1659647986,
                "carousel": carousel,
                "title": title,
                "message": message,
                "trid": trid,
                "customPayload": {}
            },
            "trid": trid
        },
        "priority": 0
    }

    print(payload)
    response = requests.request("POST", FCM_URL, data=json.dumps(payload), headers=headers)
    print(response.text)
    return response.json()