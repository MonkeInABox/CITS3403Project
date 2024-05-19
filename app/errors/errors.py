from flask import render_template
from app import db
from app.errors import bp
from app.main.forms import FilterForm, SearchForm

@bp.app_errorhandler(404)
def not_found_error(error):
    filter_form = FilterForm()
    search_form = SearchForm()
    return render_template('404.html', form=search_form), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500