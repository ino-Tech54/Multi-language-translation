from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import func, desc

import os
import requests

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


