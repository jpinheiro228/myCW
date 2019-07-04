from website.models import db, User, Exercise, ExerciseSolution


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


def get_all_users():
    """

    :return:
    """
    users = User.query.all()
    users_dict = []
    for i in users:
        users_dict.append({"id": i.id, "name": i.username})

    return users_dict


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


def edit_user_pwd(username=None, new_pass=None):
    """

    :param username:
    :param hashed_password:
    :return:
    """
    error = None
    user = User.query.filter_by(username=username).first()
    if user:
        user.password = new_pass
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


def get_exercise_solution(exercise_id=None,user=None):
    if exercise_id:
        ex = ExerciseSolution.query.filter_by(exercise=int(exercise_id),
                                              user=int(user)).first()
        return ex
    return None


def update_exercise_solution(exercise_id=None, user=None, new_code=None):
    ex = None
    if exercise_id:
        ex = ExerciseSolution.query.filter_by(exercise=int(exercise_id),
                                              user=int(user)).first()
    if ex:
        ex.code = new_code
    else:
        ex = ExerciseSolution(exercise=int(exercise_id),
                              user=int(user),
                              code=new_code)
        db.session.add(ex)
    db.session.commit()
    return ex


def add_exercise(description="", test_code="", check_code=""):
    error = None
    ex = Exercise(description, test_code, check_code)  # Test Exercise
    db.session.add(ex)

    try:
        db.session.commit()
    except Exception as e:
        error = str(e)
    return error


def rm_exercise(id):
    error = None

    try:
        exercise = Exercise.query.filter_by(id=id).first()
        if exercise:
            db.session.delete(exercise)
            ####################################################################
            #                Remove all related solutions                      #
            solutions = ExerciseSolution.query.filter_by(exercise=id).all()
            for i in solutions:
                db.session.delete(i)
            ####################################################################
            db.session.commit()
        else:
            raise Exception("Exercise not found.")
    except Exception as e:
        error = str(e)

    return error


def get_all_exercises():
    exercises = Exercise.query.all()
    exercises_dict = []
    for i in exercises:
        exercises_dict.append({"id": i.id, "description": i.description,
                               "test_code": i.test_code, "check_code": i.check_code})

    return exercises_dict


def edit_exercise(exercise_id=None, description="", test_code="", check_code=""):
    error = None
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    if exercise:
        exercise.description = description
        exercise.test_code = test_code
        exercise.check_code = check_code
        try:
            db.session.commit()
        except Exception as e:
            error = str(e)

    return error


def get_all_solutions():
    solutions = ExerciseSolution.query.all()
    solutions_dict = []
    for i in solutions:
        solutions_dict.append({"id": i.id,
                               "exid": i.exercise,
                               "user": get_user(user_id=i.user).username,
                               "user_id": i.user,
                               "solution": i.code})

    return solutions_dict