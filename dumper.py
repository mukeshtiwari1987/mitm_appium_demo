from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import http
from mitmproxy.addons import block
import json


mitmproxy_conf = '/home/mukesh.tiwari/.mitmproxy'

netcore_url = "pn.netcoresmartech.com"  # URL to be sniffed
pn_reg_url = netcore_url+ "/pn_register"


class NetcoreSniffer:

    def request(self, flow: http.HTTPFlow):
        if netcore_url in flow.request.pretty_url:
            print("BODY ---> {}".format(str(flow.request.content)))
        content = flow.request.content.decode("utf-8")
        if content:
            save_request_as_json(content)


def save_request_as_json(self, content):
    content = content.split('=')
    after_data = content[1]
    with open("pn_register.json", "w") as write_file:
        json.dump(after_data, write_file)


ncore_sniff_addon = NetcoreSniffer()
opts = options.Options(listen_host='0.0.0.0', listen_port=8080, mode='transparent', confdir=mitmproxy_conf)
pconf = proxy.config.ProxyConfig(opts)
m = DumpMaster(opts)
m.addons.add(block)
m.addons.add(ncore_sniff_addon)
m.options.set('block_global=false')
m.server = proxy.server.ProxyServer(pconf)



# try:
#     m.run()
# except KeyboardInterrupt:
#     m.shutdown()