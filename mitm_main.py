import json
from mitmproxy import http

pn_reg_url = "https://pn.netcoresmartech.com/pn_register"
pn_delivery_url = "https://pn.netcoresmartech.com/pn_deliver"
pn_open_url = "https://pn.netcoresmartech.com/pn_open"
# pn_rules_url = "https://pnrules.netcoresmartech.com/inappactivity/903c8fa4dcf982b0626b48a1a932fb1a.json"
# pn_rule_inapp_url = "https://pnrules.netcoresmartech.com/inapp?clientid=71564&id=21"
# pn_app_activity_url = "https://pn.netcoresmartech.com/app_activity"
drop_mitm_ncore = "dropmitmncore1.requestcatcher.com"


def request(flow: http.HTTPFlow):
    if flow.request.pretty_url in [pn_reg_url, pn_delivery_url, pn_open_url]:
        print("BODY ---> {}".format(str(flow.request.content)))
        content = flow.request.content.decode("utf-8")
        if content:
            save_pn_as_json(content, flow.request.pretty_url.split('/')[3])
        flow.request.host = drop_mitm_ncore


def save_pn_as_json(content, url_endpoint):
    content_before_data = content.split('=')
    content_after_data = content_before_data[1]
    with open(url_endpoint + ".json", "w") as write_file:
        json.dump(content_after_data, write_file)


# def response(flow):
#     with open("response.txt", "w") as ofile:
#         ofile.write(flow.request.pretty_url)
#
#         if flow.request.content:
#             ofile.write(flow.request.content)
#
#         if flow.response.content:
#             ofile.write(flow.response.content)

