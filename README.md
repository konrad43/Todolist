# Todolist

A todolist with simple API. It shows a list of tasks and enables to add, update and delete tasks

## Endpoints

**/todolist - allows GET and POST**

GET:
    Displays a todolist in JSON format from database
    :returns JSON object
    
POST:
    Adds a new task from request
    :returns new task id in JSON
    
**/todolist/<int:task_id> - allows  GET, PATCH and DELETE**

GET:
    :returns a task with a given id in JSON format

PATCH:
    updates data in database from request
    :returns 204
    
DELETE:
    deletes item from database
    :returns 204
