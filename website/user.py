from flask import (Blueprint, flash, redirect,
                   render_template, request, url_for,
                   abort, session)

from website import db_utils
from website.auth import login_required
import os
import docker_control as dc

dir_path = os.path.dirname(os.path.realpath(__file__))

bp = Blueprint('user', __name__, url_prefix='/my_home')


@bp.route("/")
@login_required
def main_page():
    return render_template("user/main.html",
                           current_exercise=db_utils.get_current_exercise_id(
                               user_id=session["user_id"]))


@bp.route("/list", methods=["GET", "POST"])
@login_required
def list_exercises():
    if request.method == "GET":
        return render_template("user/list.html")
    else:
        return abort(501)


@bp.route("/exercise", methods=["GET", "POST"])
@login_required
def exercise():
    exercise_id = request.args.get('exercise_id')
    output = request.args.get('output')

    if not exercise_id:
        exercise_id = db_utils.get_current_exercise_id(user_id=session["user_id"])
    ex = db_utils.get_exercise(int(exercise_id))
    ex_sol = db_utils.get_exercise_solution(exercise_id=int(exercise_id),
                                            user=session["user_id"])
    my_solution = ""
    if ex_sol:
        my_solution = ex_sol.code

    if request.method == "POST":
        sub_type = request.form["sub_type"]
        my_solution = request.form["my_solution"]
        if sub_type == "test":
            exec_code = ex.test_code
        else:
            exec_code = ex.check_code

        output = dc.run_code(code=my_solution, test_code=exec_code, user=session["username"])
        db_utils.update_exercise_solution(exercise_id, session["user_id"], my_solution)

    return render_template("user/exercise.html",
                           description=ex.description,
                           test_code=ex.test_code,
                           my_solution=my_solution,
                           output=output,
                           exercise_id=exercise_id)
