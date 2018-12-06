from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import requests
 
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
 
def getExchangeRates():
    temp = []
    sound = []
    new_params = {
  "id": "Postman Testing",
  "method": "down.query_data",
  "params": {
    "limit":20,
    "order_by":"timestamp",
    "direction":"DESC"
  }
  }
    response = requests.post('http://davidkopala.com:8000/api',json.dumps(new_params))
    
    data = response.text
    print (data)
    rdata = json.loads(data, parse_float=float)
    for j in rdata['result']['raw']:
      if j['type'] == 'Temperature':
        temp.append(j['value'])
      if j['type'] == 'Sound':
        sound.append(float(j['value'])*100)
    return temp , sound
 
@app.route("/")
def index():
    temp , sound = getExchangeRates()
    return render_template('test.html',**locals())      
 
@app.route("/hello")
def hello():
    return "Hello World!"
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
