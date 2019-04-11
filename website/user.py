from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, abort, session
)

from website import db_utils
from website.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/my_home')


@bp.route("/")
@login_required
def main_page():
    return render_template("user/main.html", current_exercise=db_utils.get_current_exercise_id(user_id=session["user_id"]))


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
    if request.method == "GET":
        desc = ex.description
        test_code = ex.test_code
        return render_template("user/exercise.html", description=desc, test_code=test_code)
    elif request.method == "POST":
        check_code = ex.check_code
    else:
        return abort(501)
