from flask import Blueprint

bp = Blueprint('comments', __name__, template_folder="templates")

from app.comments import routes