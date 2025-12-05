from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User
import requests
from sqlalchemy import func
import json

user_bp = Blueprint('user', __name__, url_prefix='/user')

