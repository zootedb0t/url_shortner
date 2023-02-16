import os
import pyqrcode
from flask import (
    render_template,
    request,
    redirect,
    make_response,
    send_from_directory,
)
import requests
import json
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
    return response


@app.route("/shortner", methods=["POST", "GET"])
def shortner():
    # TODO: Find another way to do this. Instead of hard coding
    bitlyKey = Key.query.filter_by(id=1).first()
    # Show message when no api-key is found.
    if bitlyKey is None:
        return "Please add api key"
    else:
        key = bitlyKey.auth_key
        gid = bitlyKey.grp_id
    if request.method == "POST":
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
    # Another way to do this

    # conn = sqlite3.connect("your database")
    # cur = conn.cursor()
    # url = cur.execute("SELECT * FROM url").fetchall()
    # conn.close()

    # A better way
    url = Url.query.all()
    return render_template("database.html", url=url)


@app.route("/addkey")
def keyform():
    key = Key.query.all()
    return render_template("addkey.html", key=key)


@app.route("/addkey", methods=["POST"])
def addkey():
    name = request.form["name"]
    apikey = request.form["apikey"]
    groupid = request.form["groupid"]
    if request.method == "POST":
        if Key.query.filter_by(auth_key=apikey).first():
            return "Api key already present!!"
        else:
            new_key = Key(name=name, auth_key=apikey, grp_id=groupid)
            db.session.add(new_key)
            db.session.commit()
    return render_template("index.html")


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
    url = data.short_url
    qr_obj = pyqrcode.create(url)
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


@app.route("/deletekey/<int:id>")
def deletekey(id):
    data = Key.query.get(id)
    print(data)
    db.session.delete(data)
    db.session.commit()
    return render_template("addkey.html")


@app.route("/copytoclipboard/<int:id>")
def copytoclipboard(id):
    data = Url.query.filter_by(id=id).first()
    url = data.short_url
    return render_template("copy.html", bitly_url=url)


@app.errorhandler(500)
def basic_error(e):
    error_msg = e
    return render_template("500.html", error_message=error_msg)
