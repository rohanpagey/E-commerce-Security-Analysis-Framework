"""Take incoming HTTP requests and replay them with modified parameters (session)."""

import toml
from mitmproxy import ctx

##################### CONFIG ########################
config = toml.load('config.toml')

api_host = config["parameter"]["api_host"]
replace_header = config["parameter"]["replace_header"]
modified_session = config["parameter"]["modified_session"]

##################### CONFIG ########################

def request(flow):
    
    if flow.is_replay == "request" or flow.request.host != api_host:
        return
    
    if unsafeIdempotent(flow):
        flow.request.headers["Cookie"] = modified_session
        return
    
    flow = flow.copy()
    
    if "view" in ctx.master.addons:
        ctx.master.commands.call("view.flows.add", [flow])

    flow.request.headers[replace_header] = modified_session

    ctx.master.commands.call("replay.client", [flow])


def unsafeIdempotent(flow):
    if flow.request.method == "DELETE":
        return True
    """
    if flow.request.method == "POST":
        if(any(keyword in flow.request.url for keyword in keywords)):
            return True
    """