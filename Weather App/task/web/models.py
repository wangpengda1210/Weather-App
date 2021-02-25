from exts import db


class City(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
