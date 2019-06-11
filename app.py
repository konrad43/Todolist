# -*- coding: utf-8 -*-

from flask import Flask, request, abort, jsonify

from db import init_db_command, db_session
from models import ToDo

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/todolist', methods=('GET', 'POST'))
def todolist():
    """Displays a todolist and enable to add tasks

    Methods
    -------
    GET:
        Displays a todolist in JSON format from database
        :returns JSON object
    POST:
        Adds a new task from request
        :returns new task id in JSON
    """
    if request.method == 'GET':
        data = db_session.query(ToDo).all()
        json_data = get_json_tasks(data)
        return jsonify(json_data)

    elif request.method == 'POST':
        try:
            task_data = get_task_data(request)
        except TypeError as e:
            return 'Unvalid data: {}'.format(e)

        task = ToDo(title=task_data['title'],
                    done=task_data['done'],
                    done_date=task_data['done_date'],
                    author_ip=task_data['author_ip'])

        db_session.add(task)
        db_session.commit()

        return jsonify({'task_id': task.id})
    abort(405)


def get_task_data(request):
    """Validates data from request and creates a dict

    :param request:
    :return:
        A dict with fields to be added to database
    """
    data = request.json
    done_date, done, done_false = 0,0,0

    if not data.get('title'):
        raise TypeError('"title" is required')

    task = dict(
        title=data.get('title'),
        done=data.get('done'),
        done_date=data.get('done_date'),
        author_ip=request.remote_addr,
        done_false=done_false
    )
    if task['done'] == False:
        task['done_false'] = 1

    if task['done']:
        task['done'] = 1
        if not task['done_date']:
            task['done_date'] = get_done_date()
    else:
        task['done'] = 0
        if task['done_date']:
            return '', 400
    return task


def json_dict(task):
    """Converts database data to dict"""
    json_db = {}
    json_db['id'] = task.id
    json_db['title'] = task.title
    json_db['done'] = bool(task.done)
    json_db['author_ip'] = task.author_ip
    json_db['created_date'] = str(task.created_date)
    json_db['done_date'] = task.done_date
    return json_db


def get_json_tasks(tasks):
    """Converts ToDo database object to list"""
    db_list = []
    keys = ['id', 'title', 'done', 'author_ip', 'created_date', 'done_date']
    for task in tasks:
        json_db = json_dict(task)
        db_list.append(json_db)
    return db_list


def get_done_date():
    """Parse done_date to suitable format"""
    return (
        datetime.datetime.utcnow()
            .strftime('%Y-%m-%d %H:%M:%S')
    )


app.cli.add_command(init_db_command)

if __name__ == '__main__':
    app.run(debug=True)
