from flask import Flask
from config import Config
from models import db, init_db
from flask_login import LoginManager
from views.auth import auth_bp
from views.user import user_bp
from views.translate import trans_bp
from views.admin import admin_bp


app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

init_db(app) 
login_manager.init_app(app)
    

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(trans_bp, url_prefix ='/trans')


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
 
    app.run(host='0.0.0.0', port=5000, debug=True)