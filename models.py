from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def zimbabwe_now():
    harare_tz = pytz.timezone("Africa/Harare")
    return datetime.now(harare_tz)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    created_at = db.Column(db.DateTime, default=zimbabwe_now)

    # Relationships
    uploads = db.relationship("MediaFile", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name}>"


class MediaFile(db.Model):
    __tablename__ = "media_files"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  
    file_type = db.Column(db.String(50), nullable=False)  
    original_language = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=zimbabwe_now)

    def __repr__(self):
        return f"<MediaFile {self.filename}>"


class Translation(db.Model):
    __tablename__ = "translations"
    id = db.Column(db.Integer, primary_key=True)
    english_sentence = db.Column(db.Text, nullable=False)
    shona_subtitle = db.Column(db.Text, nullable=True)      
    shona_translation = db.Column(db.Text, nullable=False)
    ndebele_subtitle = db.Column(db.Text, nullable=True)    
    ndebele_translation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=zimbabwe_now)

class LiveTranslation(db.Model):
    __tablename__ = "live_translations"
    id = db.Column(db.Integer, primary_key=True)
    translation_id = db.Column(db.Integer, db.ForeignKey("translations.id"), nullable=True)  # <-- nullable now
    selected_language = db.Column(db.String(10), nullable=False)  # 'shona' or 'ndebele'
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, default=zimbabwe_now)
    end_time = db.Column(db.DateTime, default=zimbabwe_now)

    translation = db.relationship("Translation", backref="live_translations")


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        #db.drop_all()
