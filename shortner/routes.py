from shortner import app, db, Url
import sqlite3

from flask import render_template, request
import requests
import json

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shortner", methods=["POST"])
def shortner():
    form_url = request.form["data"]
    if form_url.startswith("https://"):
        url = form_url
    else:
        url = "https://" + form_url
    headers = {
        "Authorization": "your auth key",
        "Content-Type": "application/json",
    }
    raw_data = {"long_url": url, "group_guid": "your group id"}
    data = json.dumps(raw_data, indent=2)
    response = requests.post(
        "https://api-ssl.bitly.com/v4/shorten", headers=headers, data=data
    ).json()
    format = json.dumps(response, indent=2)
    short_link = json.loads(format)["link"]

    if form_url != '' and short_link != '':
        p = Url(actual_url=form_url, short_url=short_link)
        db.session.add(p)
        db.session.commit()
    return short_link

@app.route("/database")
def get_url():
    conn = sqlite3.connect('database file')
    cur = conn.cursor()
    url = cur.execute('SELECT * FROM url').fetchall()
    conn.close()
    return render_template("database.html", url=url)
