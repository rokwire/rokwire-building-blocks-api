import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .config import Config
# from ..api.controllers.contributions import client_contribution, db_contribution, coll_contribution, post, get, put, search, delete

bp = Blueprint('contribute', __name__, url_prefix='/contribute')

@bp.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
    #     title = request.form['title']
    #     body = request.form['body']
    #     error = None
    #
    #     if not title:
    #         error = 'Title is required.'
    #
    #     if error is not None:
    #         flash(error)
    #     else:
    #         db = get_db()
    #         db.execute(
    #             'INSERT INTO post (title, body, author_id)'
    #             ' VALUES (?, ?, ?)',
    #             (title, body, g.user['id'])
    #         )
    #         db.commit()
    #         return redirect(url_for('blog.index'))

    return render_template('contribute/home.html')

@bp.route('/create', methods=['GET', "POST"])
def create():
    if request.method == 'POST':
        result = request.form
        print(result)
    #     # body = request.form['body']
    #     # post()
    return render_template('contribute/contribute.html')