import os
import json
import pyqrcode
from flask import (
    render_template,
    request,
    make_response,
    send_from_directory,
)
import requests
from shortner import app

# Database related stuff
from shortner.model import Url, Key, db


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
    # response for setting cookie
    response = make_response(render_template("index.html"), 200)
    response.set_cookie("message", "Cookie time", samesite="Lax")
    apikeys = Key.query.all()
    if len(apikeys) == 0:
        return render_template("index.html", apikeys="")
    return render_template("index.html", apikeys=apikeys)


@app.route("/shortner", methods=["POST", "GET"])
def shortner():
    # Show message when no api-key is found.
    if request.method == "POST":
        bitly_key = Key.query.all()
        if len(bitly_key) == 0:
            return render_template("error.html", message="Please add api key.")
        # else:
        activeid = request.form["currentapikey"]
        bitly_key = Key.query.filter_by(id=activeid).first()
        key = bitly_key.auth_key
        gid = bitly_key.grp_id
        url = request.form["data"]
        headers = {
            "Authorization": key,
            "Content-Type": "application/json",
        }
        raw_data = {"long_url": url, "group_guid": gid}
        # response returns a object after request. To get relevant data you need to
        # access the property you're after, e.g. r.status_code, r.text, etc.
        # response has type dictionary
        response = requests.post(
            "https://api-ssl.bitly.com/v4/shorten",
            headers=headers,
            # Conversion from python to json
            data=json.dumps(raw_data),
        )
        data = response.json()
        # Check server response code
        if response.status_code == 200:
            # Conversion from python dictionary to json
            data_format = json.dumps(data, indent=2)
            short_link = json.loads(data_format)["link"]
        else:
            return render_template("error.html", message="Something went wrong!!")

        # Check for duplicates
        if url != "" and short_link != "":
            if Url.query.filter_by(actual_url=url).first():
                return render_template("duplicate.html", duplicate=url)
            # Add url to database
            p = Url(actual_url=url, short_url=short_link)
            db.session.add(p)
            db.session.commit()
        return render_template("slink.html", link=short_link)
    return render_template(
        "error.html", message="Please use POST method GET is not allowed."
    )


@app.route("/database")
def database():
    # Another way to do this

    # conn = sqlite3.connect("your database")
    # cur = conn.cursor()
    # url = cur.execute("SELECT * FROM url").fetchall()
    # conn.close()

    # A better way
    url = Url.query.all()  # url is list
    if len(url) == 0:
        return render_template("error.html", message="Database is empty. Add some url.")
    return render_template("database.html", url=url)


@app.route("/addkey", methods=["POST", "GET"])
def addkey():
    if request.method == "POST":
        name = request.form["name"]
        apikey = request.form["apikey"]
        groupid = request.form["groupid"]
        if Key.query.filter_by(auth_key=apikey).first():
            return "Api key already present!!"
        new_key = Key(name=name, auth_key=apikey, grp_id=groupid)
        db.session.add(new_key)
        db.session.commit()
        key = Key.query.all()
        return render_template("addkey.html", key=key)
    key = Key.query.all()
    return render_template("addkey.html", key=key)


@app.route("/qrcode/<int:url_id>")
def getqr(url_id):
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
    data = Url.query.filter_by(id=url_id).first()
    url = data.short_url
    qr_obj = pyqrcode.create(url)
    # qr_code = qr_obj.png("file.png", scale=10, background="#FFFFFF")
    image_as_str = qr_obj.png_as_base64_str(scale=10)

    image = f"data:image/png;base64,{image_as_str}"
    return render_template("qrcode.html", qrcode=image)


@app.route("/deleteurl/<int:url_id>", methods=["POST"])
def deleteurl(url_id):
    data = Url.query.get(url_id)
    db.session.delete(data)
    db.session.commit()
    url = Url.query.all()
    return render_template("database.html", url=url)


@app.route("/deletekey/<int:key_id>", methods=["POST"])
def deletekey(key_id):
    data = Key.query.get(key_id)
    db.session.delete(data)
    db.session.commit()
    key = Key.query.all()
    return render_template("addkey.html", key=key)


@app.route("/copytoclipboard/<int:url_id>")
def copytoclipboard(url_id):
    data = Url.query.filter_by(id=url_id).first()
    url = data.short_url
    return render_template("copy.html", bitly_url=url)


@app.route("/query", methods=["POST"])
def search_database():
    search_query = request.form["query"]
    match = Url.query.filter(
        Url.actual_url.contains(search_query)
    ).all()  # This returns a list

    if len(match) == 0:
        return render_template("error.html", message="No match found!")
    return render_template("database.html", url=match)


@app.errorhandler(500)
def basic_error(e):
    error_msg = e
    return render_template("error.html", message=error_msg)
