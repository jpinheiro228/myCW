from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, abort, session
)

from website import db_utils
from website.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/clients')


# Clients Functions
@bp.route("/")
@login_required
def main_page():
    return render_template("user/main.html", current_exercise=db_utils.get_current_exercise_id(session["user_id"]))


@bp.route("/list", methods=["GET", "POST"])
@login_required
def list_exercises():
    if request.method == "GET":
        return render_template("user/list.html")
    else:
        return abort(501)


@bp.route("/exercise", methods=["GET", "POST"])
@login_required
def exercise(client_id):
    if request.method == "GET":
        client = db_utils.get_clients(client_id)
        return render_template("user/client_rm.html", client=client)
    elif request.method == "POST":
        error = db_utils.rm_client(client_id)
        if error:
            flash(error, category="danger")
        return redirect(url_for("user.clients"))
    else:
        return abort(501)
