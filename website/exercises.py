import functools

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session,
                   url_for, abort)

from website import db_utils
import os
import docker_control as dc

bp = Blueprint('exercises', __name__, url_prefix='/exercises')

dir_path = os.path.dirname(os.path.realpath(__file__))


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


@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
    if session["user_id"] == 1:
        if request.method == 'POST':
            description = request.form['description']
            test_code = request.form['test_code']
            validation_code = request.form['validation_code']

            error = db_utils.add_exercise(description, test_code, validation_code)

            if error is None:
                flash("Exercise successfully registered.", category="success")
                return redirect(url_for('exercises.list'))
            flash(error, category="danger")

        return render_template('exercises/new.html')
    return abort(401)


@bp.route('/edit/<exercise_id>', methods=('GET', 'POST'))
@login_required
def edit(exercise_id):
    if session["user_id"] == 1:
        if request.method == "POST":
            description = request.form['description']
            test_code = request.form['test_code']
            validation_code = request.form['validation_code']
            error = db_utils.edit_exercise(exercise_id, description, test_code, validation_code)
            if error is None:
                flash("Exercise successfully updated.", category="success")
                return redirect(url_for('exercises.list'))
            flash(error, category="danger")

        elif request.method == "GET":
            ex = db_utils.get_exercise(exercise_id)
            return render_template('exercises/edit.html', ex=ex)
        return redirect(url_for('exercises.list'))
    return abort(401)


@bp.route('/remove/<exercise_id>', methods=('GET', 'POST'))
@login_required
def remove(exercise_id=None):
    if session["user_id"] == 1:
        if request.method == 'POST':
            db_utils.rm_exercise(request.form['rm_id'])
            return redirect(url_for('exercises.list'))
        elif request.method == "GET":
            if exercise_id:
                rm_exercise = db_utils.get_exercise(exercise_id=exercise_id)
                return render_template("exercises/rm.html", exercise=rm_exercise)
            return redirect(request.referrer)
    return abort(401)


@bp.route('/list')
@login_required
def list():
    exercise_list = db_utils.get_all_exercises()
    return render_template('exercises/list.html', exercise_list=exercise_list)


@bp.route('/solution_list')
@login_required
def solution_list():
    if session["user_id"] == 1:
        solution_list = db_utils.get_all_solutions()
        return render_template('exercises/solution_list.html', solution_list=solution_list)
    return abort(401)


@bp.route('/solution_view/<user>/<id>', methods=('GET', 'POST'))
@login_required
def solution_view(user, id):
    if session["user_id"] == 1:
        output = request.args.get('output')
        solution = db_utils.get_exercise_solution(exercise_id=id, user=user)
        ex = db_utils.get_exercise(int(id))
        username = db_utils.get_user(user_id=user).username
        if request.method == "POST":
            output = dc.run_code(code=solution.code, test_code=ex.check_code, user=session["username"])
        return render_template('exercises/solution_view.html', solution=solution, output=output, username=username)

    return abort(401)




