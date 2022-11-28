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
    url = request.form['data']
    url_secure = "https://" + url
    headers = {
        'Authorization': '9a02ca6a0051dc7d0af541e95e6f6c1f26704c2a',
        'Content-Type': 'application/json',
    }
    data = '{ "long_url": "https://www.google.com", "group_guid": "Bl7ibQEpEmV" }'
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    return response.json()
    # value = response.json()
    # json_format = json.dump(value, indent=2)
    # return json.load(json_format)
    # json_output = json.load(json_format)
    # return json.dumps(response.json(), indent=2)
