"""
    Returns the total number of URLs in original.flow file
"""
from mitmproxy.io import FlowReader
from mitmproxy.addons import export
import webbrowser,json
import toml

##################### CONFIG ########################
config = toml.load('config.toml')

api_host = config["parameter"]["api_host"]
filename = config["files"]["main_file"]
##################### CONFIG ########################


def verCount():
    with open(filename, 'rb') as fp:
        reader = FlowReader(fp)
        orgCount=0
        modCount=0
        for flow in reader.stream():

            if flow.request.host == api_host and flow.is_replay == "request":
                modCount=modCount+1
            if flow.request.host == api_host and flow.is_replay != "request":
                orgCount=orgCount+1
    return orgCount
