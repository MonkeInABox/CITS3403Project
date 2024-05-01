from flask import Blueprint

bp = Blueprint('posts', __name__, template_folder="templates")

from app.posts import routes