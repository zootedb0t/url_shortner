from shortner import app
from flask import render_template
from flask import request
import requests
import json

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/shortner', methods=['POST'])
def shortner():
    url = "https://" + request.form['data']
    headers = {
        'Authorization': 'enter your token',
        'Content-Type': 'application/json',
    }
    raw_data = { "long_url": url, "group_guid": "enter your group id"  }
    data = json.dumps(raw_data, indent=2)
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    value = response.json()
    format = json.dumps(value, indent=2)
    output = json.loads(format)
    return output['link']
