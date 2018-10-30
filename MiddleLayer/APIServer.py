import traceback
import os

from flask import Flask
from flask import request
from flask import send_from_directory

from RPCObjects import *
from APIRouter import Router

"""
Flask is a python library for responding to HTTP requests
http://flask.pocoo.org/docs/1.0/quickstart/

This class sets up the entry point for the API, but should
not contain any actual information and data handling. These
should be done in a separate class and imported into this one. 
"""

# Global Debug Variable; Defines if verbose logging should be enabled
debug = True

# Create a GLOBAL instance of the router
#   This will cause it to maintain its state between requests
router = Router()

# Create a Flask Object.
app = Flask(__name__)


# This is a decorator; basically provides more metadata about the function
# app.route([route]) tells Flask that the following function should be
#     executed when a client sends a request to [route].
#     Flask collects the response (cannot be None) and sends that to the client
@app.route('/test')
def index():
    return 'Hello World!'

@app.route('/<path:path>')
def path(path):
    root_dir = os.path.dirname(os.getcwd())
    root_dir = os.path.join(root_dir, 'MiddleLayer')
    print root_dir + '/' + path
    return send_from_directory(root_dir, path)


# This is the route for all API calls
# This function expects a Json RPC object to be send in one of the following places:
#     post body data
#     get 'r' variable; ie /?r={}
#     form-data 'r' variable
# For accessing request data: https://stackoverflow.com/a/16664376
@app.route('/api', methods=["GET", "POST"])
def handle_request():
    if request.args.has_key("r"):
        data = request.args["r"]
        if debug: print "Found JSON RPC Request in GET Variables!"
    elif request.form.get("r"):
        data = request.form["r"]
        if debug: print "Found JSON RPC Request in FORM Variables!"
    else:
        data = request.data
        if debug: print "Found JSON RPC Request in POST Data!"
    try:
        # Parse the request
        req = JsonRpcRequest(data)
        # Handle the request
        ret = router.run(req)

        # Make the response
        resp = JsonRpcResponse()
        resp['id'] = req.id
        resp.load_success(ret)

        # Return the response
        return json.dumps(resp)
    except Exception as exc:
        if debug: traceback.print_exc()

        # Make the response
        errResp = JsonRpcResponse()
        errResp.load_error(exc)

        # Return the response
        return json.dumps(errResp)


# If the script is run from the command line
if __name__ == "__main__":
    # Start a development server on port 8000
    # http://localhost:8000/test
    app.run(host="0.0.0.0", port=8000, debug=True)
