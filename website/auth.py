import functools

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session,
                   url_for, abort)
from werkzeug.security import check_password_hash, generate_password_hash

from website import db_utils

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_utils.get_user(user_id=user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    if session["user_id"] == 1:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            else:
                error = db_utils.add_user(username=username, hashed_password=generate_password_hash(password))

            if error is None:
                flash("User successfully registered.", category="success")
                return redirect(url_for('auth.register'))

            flash(error, category="danger")

        return render_template('auth/register.html')
    return abort(401)


@bp.route('/myaccount', methods=('GET', 'POST'))
@login_required
def myaccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            error = db_utils.edit_user_pwd(username=username, new_pass=generate_password_hash(password))

        if error is None:
            flash("Password changed successfully.", category="success")
            return redirect(url_for('auth.myaccount'))

        flash(error, category="danger")

    return render_template('auth/myacc.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db_utils.get_user(username=username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/list')
@login_required
def list():
    if session["user_id"] == 1:
        user_list = db_utils.get_all_users()
        return render_template('auth/list.html', user_list=user_list)
    return abort(401)


@bp.route('/remove/<rm_id>', methods=('GET', 'POST'))
@login_required
def remove(rm_id=None):
    if session["user_id"] == 1:
        if request.method == 'POST':
            db_utils.rm_user(request.form['rm_id'])
            return redirect(url_for('auth.list'))
        elif request.method == "GET":
            if rm_id:
                rm_user = db_utils.get_user(user_id=rm_id)
                return render_template("auth/rm.html", user=rm_user)
            return redirect(request.referrer)
    return abort(401)