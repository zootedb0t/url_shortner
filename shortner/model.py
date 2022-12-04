from shortner import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actual_url = db.Column(db.String(120), index=True, unique=True)
    short_url = db.Column(db.String(60), index=True, unique=True)

    def __repr__(self):
        return f"URL : {self.actual_url}, Short: {self.short_url}"
