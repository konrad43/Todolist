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


app.cli.add_command(init_db_command)

if __name__ == '__main__':
    app.run(debug=True)
