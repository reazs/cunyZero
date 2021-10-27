from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)
app.secret_key = "fjkasdhf@#$RAEFaf23"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFACTIONS"] = False  
db = SQLAlchemy(app)
from cunyzero import routes

