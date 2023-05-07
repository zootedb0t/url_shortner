"""Import db object"""
from flask_sqlalchemy import SQLAlchemy
from shortner import app

db = SQLAlchemy(app)


class Url(db.Model):
    """URL Database"""

    id = db.Column(db.Integer, primary_key=True)
    actual_url = db.Column(db.String(120), index=True, unique=True)
    short_url = db.Column(db.String(60), index=True, unique=True)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return (
            f"ID: {self.id}, Bitly URL : {self.actual_url}, Short URL: {self.short_url}"
        )

    def __str__(self):
        return f"Bitly URL is {self.actual_url} and original URL is {self.short_url} "


class Key(db.Model):
    """API Key"""

    __bind_key__ = "key"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    auth_key = db.Column(db.String(120), index=True, unique=True)
    grp_id = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return f"ID: {self.id}, Auth Key: {self.auth_key}, Group Id: {self.grp_id}"

    def __str__(self):
        return f"""Key name is {self.name}, authorization-key is {self.auth_key}
         and group-id is {self.grp_id}"""
