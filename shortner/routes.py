from shortner import app
from shortner.model import Url, db
import sqlite3
from flask import render_template, request, redirect
import requests
import json
import api


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shortner", methods=["POST", "GET"])
def shortner():
    if request.method == "POST":
        form_url = request.form["data"]
        if form_url.startswith("https://"):
            url = form_url
        else:
            url = "https://" + form_url
        headers = {
            "Authorization": api.Authorization,
            "Content-Type": "application/json",
        }
        raw_data = {"long_url": url, "group_guid": api.group_guid}
        response = requests.post(
            "https://api-ssl.bitly.com/v4/shorten",
            headers=headers,
            data=json.dumps(raw_data),
        ).json()
        format = json.dumps(response, indent=2)
        short_link = json.loads(format)["link"]

        # Check for duplicates
        if form_url != "" and short_link != "":
            p = Url(actual_url=form_url, short_url=short_link)
            db.session.add(p)
            db.session.commit()
        return render_template("slink.html", link=short_link)
    else:
        return "Please use POST method GET is not allowed"


@app.route("/database")
def get_url():
    conn = sqlite3.connect(
        "/home/stoney/Documents/Projects/url_shortner/instance/url.db"
    )
    cur = conn.cursor()
    url = cur.execute("SELECT * FROM url").fetchall()
    conn.close()
    return render_template("database.html", url=url)


@app.route("/qrcode/<int:id>")
def getqr(id):
    headers = {
        "Authorization": api.Authorization,
    }
    params = (("image_format", "svg"),)
    data = Url.query.filter_by(id=id).first()
    url_secure = data.short_url
    db.session.commit()
    bit_url = url_secure.removeprefix("https://")
    r = f"https://api-ssl.bitly.com/v4/bitlinks/{bit_url}/qr"
    response = requests.get(r, headers=headers, params=params).json()
    format = json.dumps(response, indent=2)
    api_output = json.loads(format)["description"]
    return render_template("error.html", error_message=api_output)


@app.route("/delete/<int:id>")
def erase(id):
    data = Url.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/")


@app.errorhandler(500)
def basic_error(e):
    error_msg = e
    return render_template("500.html", error_message=error_msg)
