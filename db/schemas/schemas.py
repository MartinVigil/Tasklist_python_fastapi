from db.models.models import User2
from db.models.models import Task2

def user_schema(user):
    return User2(id = str(user['_id']),
                user = str(user['user']),
                hashed_password = str(user['hashed_password']),
                disabled = str(user['disabled']))

def users_schema(users):
    return [user_schema(user) for user in users]

def task_schema(task):
    return Task2(id = str(task['id']),
                task = str(task['task']),
                fk_user = str(task['fk_user']))

def tasks_schema(tasks):
    return [task_schema(task) for task in tasks]