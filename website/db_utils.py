from website.models import db, User, Exercise


def get_user(username=None, user_id=None):
    """

    :param username:
    :param user_id:
    :return:
    """
    if username:
        return User.query.filter_by(username=username).first()
    elif user_id:
        return User.query.filter_by(id=user_id).first()
    else:
        return None


def add_user(username=None, hashed_password=None):
    """

    :param username:
    :param hashed_password:
    :return:
    """
    error = None
    newuser = User(username=username,
                   password=hashed_password)
    db.session.add(newuser)
    try:
        db.session.commit()
    except Exception as e:
        error = str(e)

    return error


def rm_user(user_id):
    error = None
    if user_id == 1:
        error = "Cannot remove admin user."
    else:
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
            else:
                raise Exception("user not found.")
        except Exception as e:
            error = str(e)

    return error


def get_current_exercise_id(username=None, user_id=None):
    if username:
        return int(User.query.filter_by(username=username).first().current_exercise)
    elif user_id:
        return int(User.query.filter_by(id=user_id).first().current_exercise)
    else:
        return 0


def get_exercise(exercise_id=None):
    if exercise_id:
        ex = Exercise.query.filter_by(id=int(exercise_id)).first()
        return ex
    return None