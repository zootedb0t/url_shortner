"""Import module"""
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


@app.before_first_request
def create_tables():
    """Ensure database is created"""
    db.create_all()


# Favicon
@app.route("/favicon.ico")
def favicon():
    """Add favicon"""
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


# response for setting cookie
@app.route("/")
def home():
    """Set cookie data and check if api are present or not"""
    response = make_response(render_template("index.html"), 200)
    response.set_cookie("message", "Cookie time", samesite="Lax")
    apikeys = Key.query.all()
    if not apikeys:
        return render_template("index.html", apikeys="")
    return render_template("index.html", apikeys=apikeys)


@app.route("/shortner", methods=["POST", "GET"])
def shortner():
    """Fetch short url data from bitly server"""
    if request.method == "POST":
        bitly_key = Key.query.all()
        if not bitly_key:
            # Show message when no api-key is found.
            return render_template("error.html", message="Please add api key.")
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
        try:
            response = requests.post(
                "https://api-ssl.bitly.com/v4/shorten",
                # Conversion from python to json
                data=json.dumps(raw_data),
                headers=headers,
                # If request doesn't complete in 5sec an error will be raised
                timeout=5,
            )
        except requests.exceptions.ReadTimeout:
            return render_template(
                "error.html",
                message="""Request can't be processed. Please check your internet connection.""",
            )
        # Check server response code
        if response.status_code == 200:
            # Conversion from python dictionary to json
            data = response.json()
            data_format = json.dumps(data, indent=2)
            short_link = json.loads(data_format)["link"]
        else:
            return render_template("error.html", message="Something went wrong!!")

        # Check for duplicates
        if url != "" and short_link != "":
            if Url.query.filter_by(actual_url=url).first():
                return render_template("duplicate.html", duplicate=url)
            # Add url to database
            database_entry = Url(actual_url=url, short_url=short_link)
            db.session.add(database_entry)
            db.session.commit()
        return render_template("slink.html", link=short_link)
    return render_template(
        "error.html", message="Please use POST method GET is not allowed."
    )


@app.route("/database")
def database():
    """Display database contents"""
    # Another way to do this

    # conn = sqlite3.connect("your database")
    # cur = conn.cursor()
    # url = cur.execute("SELECT * FROM url").fetchall()
    # conn.close()

    # A better way
    url = Url.query.all()  # url is list
    if not url:
        return render_template("error.html", message="Database is empty. Add some url.")
    return render_template("database.html", url=url)


@app.route("/addkey", methods=["POST", "GET"])
def addkey():
    """Allow users to add keys via post request"""
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
    """Display qr for bitly url"""
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
    """Allow users to delete url from database"""
    data = Url.query.get(url_id)
    db.session.delete(data)
    db.session.commit()
    url = Url.query.all()
    return render_template("database.html", url=url)


@app.route("/deletekey/<int:key_id>", methods=["POST"])
def deletekey(key_id):
    """Allow users to delete api key from database"""
    data = Key.query.get(key_id)
    db.session.delete(data)
    db.session.commit()
    key = Key.query.all()
    return render_template("addkey.html", key=key)


@app.route("/copytoclipboard/<int:url_id>")
def copytoclipboard(url_id):
    """Allow users to copy short url from database"""
    data = Url.query.filter_by(id=url_id).first()
    url = data.short_url
    return render_template("copy.html", bitly_url=url)


@app.route("/query", methods=["POST"])
def search_database():
    """Search for a url in database"""
    search_query = request.form["query"]
    match = Url.query.filter(
        Url.actual_url.contains(search_query)
    ).all()  # This returns a list

    if not match:
        return render_template("error.html", message="No match found!")
    return render_template("database.html", url=match)


@app.errorhandler(500)
def basic_error(error_msg):
    """Generic error handler"""
    error = error_msg
    return render_template("error.html", message=error)


@app.errorhandler(404)
def not_found(error_msg):
    """Not found error handler"""
    error = error_msg
    return render_template("error.html", message=error)
