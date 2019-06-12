
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
