from contextlib import nullcontext
from csv import reader
from flask import Flask,render_template
from mitmproxy.io import FlowReader
from mitmproxy.addons import export
import compare,verify
import toml,operator

app = Flask(__name__)

#################################### CONFIG ######################################

#proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
config = toml.load('config.toml')

api_host = config["parameter"]["api_host"] # Main API URL
orignal_file = config["files"]["original_file"]
replayed_file = config["files"]["replayed_file"]
flow_count = verify.verCount() # value returned from count.py/2
#eliminate_urls = compare.eliminate()

#################################### CONFIG ######################################
"""
def unsafeIdempotent(flow):
    if flow.request.method == "DELETE":
        return True
    else:
        return False
"""

@app.route('/')
def index():
    with open(orignal_file, 'rb') as fp:
        reader = FlowReader(fp)
    ######################### List init starts ########################
        
        trows = flow_count
        tcols = 4
        origReq = [[0 for i in range(tcols+4)] for j in range(trows)]
        iteratorOrig = 0

    ######################### List init ends #########################

        for flow in reader.stream():
            if(flow.request.host == api_host): #and flow.request.url not in eliminate_urls): #and unsafeIdempotent(flow) == False):
                for i in range(iteratorOrig,trows):

                    origReq[i][0] = flow.request.method
                    origReq[i][1] = flow.request.url
                    if flow.response is not None:
                            origReq[i][2] = flow.response.status_code
                            origReq[i][3] = len(flow.response.content)
                    else:
                            origReq[i][2] = 0
                            origReq[i][3] = 0
                    #origReq[i][2] = flow.response.status_code
                    #origReq[i][3] = len(flow.response.content)
                    origReq[i][6] = flow.id
                    iteratorOrig = iteratorOrig + 1
                    break

# Replayed File

    with open(replayed_file, 'rb') as fp:
        reader = FlowReader(fp)
    ######################### List init starts #########################
        
        trows = flow_count
        tcols = 4
        replayReq = [[0 for i in range(tcols+1)] for j in range(trows)]
        iteratorReplay = 0

    ######################### List init ends #########################

        for flow in reader.stream():
            if(flow.request.host == api_host): # and flow.request.url not in eliminate_urls):

                if(flow.is_replay == "request"):
                    for i in range(iteratorReplay,trows):
                        replayReq[i][0] = flow.request.method
                        replayReq[i][1] = flow.request.url

                        if flow.response is not None:
                            replayReq[i][2] = flow.response.status_code
                            replayReq[i][3] = len(flow.response.content)
                        else:
                            replayReq[i][2] = 0
                            replayReq[i][3] = 0

                        replayReq[i][4] = flow.id
                        iteratorReplay = iteratorReplay + 1
                        break
        
    origReq = sorted(origReq, key = operator.itemgetter(1))
    replayReq = sorted(replayReq,key=operator.itemgetter(1))

    for i in range(0,trows):
        origReq[i][4] = replayReq[i][2]
        origReq[i][5] = replayReq[i][3]
        origReq[i][7] = str(origReq[i][6]) + "_" + str(replayReq[i][4])

        
    return render_template("index.html", origReq=origReq, replayReq=replayReq)
    #return render_template("test.html", origReq=origReq, replayReq=replayReq)
"""
def eliminate():
    with open(browsed_file, 'rb') as fp:
        reader = FlowReader(fp)
        eliminateUrls = []

        for flow in reader.stream():
            eliminateUrls.append(flow.request.url)
    return eliminateUrls
"""
@app.route('/flow/<flow_id>')
def flow(flow_id):
    origFlowId = flow_id.split('_')[0]
    modFlowId = flow_id.split('_')[1]

    with open(orignal_file, 'rb') as fp:
        reader = FlowReader(fp)
        
        origReq = []
        origResp = []

        for flow in reader.stream():

            if(flow.request.host == api_host):

                if(flow.id == origFlowId):
                    origReq.append(flow.request.method)
                    origReq.append(flow.request.path)
                    origReq.append(flow.request.http_version)
                    origReq.append(flow.request.headers.items())
                    origReq.append(flow.request.content)
                    origReq.append(flow.request.host)

                    origResp.append(flow.response.status_code)
                    origResp.append(flow.response.http_version)
                    origResp.append(flow.response.headers.items())
                    origResp.append(flow.response.content)

                    
    with open(replayed_file, 'rb') as fp:
        reader = FlowReader(fp)
        
        modReq = []
        modResp = []

        for flow in reader.stream():

            if(flow.request.host == api_host):

                if(flow.id == modFlowId):
                    modReq.append(flow.request.method)
                    modReq.append(flow.request.path)
                    modReq.append(flow.request.http_version)
                    modReq.append(flow.request.headers.items())
                    modReq.append(flow.request.content)
                    modReq.append(flow.request.host)

                    modResp.append(flow.response.status_code)
                    modResp.append(flow.response.http_version)
                    modResp.append(flow.response.headers.items())
                    modResp.append(flow.response.content)

    return render_template("flow.html", origReq = origReq, origResp = origResp, modReq= modReq, modResp= modResp)

'''
@app.route('/uir')
def uir():
    with open(orignal_file, 'rb') as fp:
        reader = FlowReader(fp)
    ######################### List init starts #########################
        

    ######################### List init ends #########################
''' 
    

if __name__ == "__main__":
    app.run(debug=True)