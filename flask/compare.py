from contextlib import nullcontext
from flask import Flask,render_template
from mitmproxy.io import FlowReader
from mitmproxy.addons import export
import os.path
#import webbrowser,json,requests

#################################### CONFIG ######################################

browsed_file = "browsed.flow"
api_host = "" # Main API URL

#################################### CONFIG ######################################

def eliminate():
    eliminateUrls = []
    if(os.path.exists(browsed_file)):
        with open(browsed_file, 'rb') as fp:
                reader = FlowReader(fp)
                for flow in reader.stream():
                    eliminateUrls.append(flow.request.url)
    else:
        eliminateUrls = []
    return eliminateUrls

# $('#data .red').length