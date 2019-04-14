from flask import (Blueprint, flash, redirect,
                   render_template, request, url_for,
                   abort, session)

from website import db_utils
from website.auth import login_required

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
    ex_id = db_utils.get_current_exercise_id(user_id=session["user_id"])
    ex = db_utils.get_exercise(int(ex_id))
    ex_sol = db_utils.get_exercise_solution(exercise_id=int(ex_id),
                                            user=session["user_id"])
    if request.method == "GET":
        desc = ex.description
        test_code = ex.test_code
        my_solution = ""
        if ex_sol:
            my_solution = ex_sol.code
        return render_template("user/exercise.html",
                               description=desc,
                               test_code=test_code,
                               my_solution=my_solution)
    elif request.method == "POST":
        sub_type = request.form["sub_type"]
        code = request.form["my_solution"]
        ex_sol = db_utils.update_exercise_solution(ex_id,
                                                   session["user_id"],
                                                   code)
        if sub_type == "test":
            test_code = ex.test_code
            pass
        elif sub_type == "final":
            check_code = ex.check_code
        return redirect(request.referrer)
    else:
        return abort(501)
