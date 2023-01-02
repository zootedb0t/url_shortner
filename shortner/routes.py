import sqlite3
import os
import pyqrcode
from flask import (
    flash,
    render_template,
    request,
    redirect,
    make_response,
    send_from_directory,
)
import requests
import json
import pyperclip
from shortner import app
from shortner.model import Url, db

# Importing private api keys
import api

# Ensure database is created
@app.before_first_request
def create_tables():
    db.create_all()


# Favicon
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/")
def home():
    response = make_response(render_template("index.html"), 200)
    response.set_cookie("message", "Cookie time")
    return response


# Authkey and group-id are stored in api.py file
@app.route("/shortner", methods=["POST", "GET"])
def shortner():
    if request.method == "POST":
        url = request.form["data"]
        headers = {
            "Authorization": api.Authorization,
            "Content-Type": "application/json",
        }
        raw_data = {"long_url": url, "group_guid": api.group_guid}
        # response returns a object after request. To get relevant data you need to
        # access the property you're after, e.g. r.status_code, r.text, etc.
        # here api returns data in json
        response = requests.post(
            "https://api-ssl.bitly.com/v4/shorten",
            headers=headers,
            # Conversion from python to json
            data=json.dumps(raw_data),
        ).json()
        # Conversion from python dictionary to json
        format = json.dumps(response, indent=2)
        short_link = json.loads(format)["link"]

        # Check for duplicates
        if url != "" and short_link != "":
            if Url.query.filter_by(actual_url=url).first():
                return render_template("duplicate.html", duplicate=url)
            else:
                p = Url(actual_url=url, short_url=short_link)
                db.session.add(p)
                db.session.commit()
        return render_template("slink.html", link=short_link)
    else:
        return "Please use POST method GET is not allowed"


@app.route("/database")
def database():
    conn = sqlite3.connect("your database")
    cur = conn.cursor()
    url = cur.execute("SELECT * FROM url").fetchall()
    conn.close()
    return render_template("database.html", url=url)


@app.route("/qrcode/<int:id>")
def getqr(id):
    # For bitly api
    #     headers = {
    #         "Authorization": api.Authorization,
    #     }
    #     params = (("image_format", "svg"),)
    #     # url_secure contains https and api only accepts url with https
    #     bit_url = url_secure.removeprefix("https://")
    #     r = f"https://api-ssl.bitly.com/v4/bitlinks/{bit_url}/qr"
    #     response = requests.get(r, headers=headers, params=params).json()
    #     format = json.dumps(response, indent=2)
    #     api_output = json.loads(format)["description"]

    # Generating qr code using pyqrcode module
    data = Url.query.filter_by(id=id).first()
    url_secure = data.short_url
    qr_obj = pyqrcode.create(url_secure)
    # qr_code = qr_obj.png("file.png", scale=10, background="#FFFFFF")
    image_as_str = qr_obj.png_as_base64_str(scale=10)

    image = "data:image/png;base64,{}".format(image_as_str)
    return render_template("qrcode.html", qrcode=image)


@app.route("/delete/<int:id>")
def delete(id):
    data = Url.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/")


@app.route("/copytoclipboard/<int:id>")
def copytoclipboard(id):
    data = Url.query.filter_by(id=id).first()
    copy = data.short_url
    pyperclip.copy(copy)
    flash("Copied to clipboard")
    return redirect("/database")


@app.errorhandler(500)
def basic_error(e):
    error_msg = e
    return render_template("500.html", error_message=error_msg)
