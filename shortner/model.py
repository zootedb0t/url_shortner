from enum import unique
from sqlalchemy import true
from sqlalchemy.sql import True_
from shortner import db


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actual_url = db.Column(db.String(120), index=True, unique=True)
    short_url = db.Column(db.String(60), index=True, unique=True)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"URL : {self.actual_url}, Short: {self.short_url}"


class Key(db.Model):
    __bind_key__ = "key"
    id = db.Column(db.Integer, primary_key=true)
    name = db.Column(db.String(120), index=true, unique=True)
    auth_key = db.Column(db.String(120), index=True, unique=True)
    grp_id = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return f"Auth-Key: {self.auth_key}, Group-Id: {self.grp_id}"
