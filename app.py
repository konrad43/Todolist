# -*- coding: utf-8 -*-

from flask import Flask, request, abort, jsonify

from db import init_db_command, db_session
from models import ToDo
from .my_functions import get_task_data, json_dict, get_json_tasks, get_done_date

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


@app.route('/todolist/<int:id>', methods=('GET','PATCH', 'DELETE'))
def update(id):
    """Enables updating and deleting data

    :param id: int

    Methods
    -------
    GET:
        :returns a task with a given id in JSON format

    PATCH:
        updates data in database from request
        :returns 204
    DELETE:
        deletes item from database
        :returns 204
    """
    try:
        data = (
            db_session.query(ToDo)
                .filter(ToDo.id == id).one()
        )
    except NoResultFound:
        return '', 404

    if request.method == 'GET':
        return jsonify(json_dict(data))

    elif request.method == 'PATCH':
        task = get_task_data(request)

        if task['title']:
            data.title = task['title']
        if task['done']:
            data.done = task['done']
        if task['done_date']:
            data.done_date = task['done_date']
        if task['done_false']:
            data.done = 0
            data.done_date = None

        db_session.add(data)
        db_session.commit()
        print('zmieniono obiekt: ',
              'tytuł: ',data.title,'done:',data.done,
              'done date: ', data.done_date,
              'flag:', task['done_false'])
        return '', 204

    elif request.method == 'DELETE':
        db_session.delete(data)
        db_session.commit()
        return '', 204

    else:
        abort(404)


app.cli.add_command(init_db_command)

if __name__ == '__main__':
    app.run(debug=True)
