from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import  ModelView


app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = "fjkasdhf@#$RAEFaf23"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFACTIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
login_manager.login_message_category = 'info'

# to avoid circular import 
from cunyzero.models import User
from CUNYZero.cunyzero.forms import CreateClassForm

admin = Admin(app, template_mode="bootstrap4")
# admin.add_view(ModelView(User, db.session))




# class CreateClassView(BaseView):
#     @expose("/")
#     def index(self):
#         form = CreateClassForm()
#         return self.render("admin/create_class.html", form=form)
#
# admin.add_view(CreateClassView(name="Create Class", endpoint="create"))

from cunyzero import routes

