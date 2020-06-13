import json
from mitmproxy import http

breakpoint_url = "netcoresmartech.com/pn_register"  # URL to be sniffed


def request(flow: http.HTTPFlow):
    if breakpoint_url in flow.request.pretty_url:
        print("BODY ---> {}".format(str(flow.request.content)))
        content = flow.request.content.decode("utf-8")
        if content:
            save_request_as_json(content)


def save_request_as_json(content):
    content = content.split('=')
    after_data = content[1]
    with open("pn_register.json", "w") as write_file:
        json.dump(after_data, write_file)


