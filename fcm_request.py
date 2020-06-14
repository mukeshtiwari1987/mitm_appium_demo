import requests
import json

FCM_URL = "https://fcm.googleapis.com/fcm/send"
FCM_KEY = "key=AAAAtJTBAjA:APA91bFArxep1J1qTLku6qDOCmZjq4a2P-HX1_tAOe8KRG0Wd_OS8mRNXxGc8YUv79dssY0ERGToO-1XkbYPOp7teafUkniRd0t8W3fp97yuiJeepMzrWB5MxnWuVUUg611-67Y7fUXP"
MY_TOKEN = "dummy_token"


def execute_rest_api(user_token,
                     image="",
                     deep_link="",
                     title=None,
                     message=None,
                     action_button=[],
                     carousel=[],
                     trid=None):

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