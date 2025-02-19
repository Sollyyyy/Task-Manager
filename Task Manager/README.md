### Overview:
Importance of Task class. The purpose of it is to create a task while having the option of manipulating it in the future through several methods
Task Manager class has the ability to build to collect all the tasks under the same object to deal with it easier through a flask application 

### Dependencies:
You need to have these libraries installed to your machine.
for the task.py
csv,pandas,sqlite3 and json
for the task_manager.py
You need csv,inspect and flask

### task.py:
It contains three classes: Task, PersonalTask and WorkTask
Task is the blue print for the other two as they inherit from it.
Task class has task_id,title, due_date, status, description and flag as it's attributes.
Task class has getters and setters for it's task_id and description. As well as a method to mark the task as completed.
PersonalTask class has an extra attribute which is priority and a setter for it.
Example: task.set_priority(priority) would check if priority is low,medium or high and it would change the priority to the new value, if it's not any of them it would return a warning to the user outputting "Invalid priority was give".

PersonalTask have a method to check if the priority is high or not as well as a setter for it.
Example: task.is_high_priority() would check if task.priority is equal to string of high and it would return a boolean according to the equating of them
PersonalTask,WorkTask have save_to_db which adds the task to a table in a database
Example: task.save_to_db() would create a table if it is not created and would output an error message if it was not possible to create a table, then it would add the task to the database, would output an error message if it wasnt possible to save the task
PerosnalTask,WorkTask have load_from_db which returns the value of the task from the database.
Example: task.load_from_db() would find the task if it is in the database else it would return a output an error message
PersonalTask,WorkTask has update_in_db which overwrites the value of the task in the table with the current one.
Example: task.update_from_db() would update the task if it is in the database else it would return a output an error message
PersonalTask,WorkTask have delete_from_db which removes the task from the database.
Example: task.delete_from_db() would delete the task if it is in the database else it would return a output an error message
WorkTask has add_team_member method which appends a team member to the object's list of team members
Both PersonalTask and WorkTask have a string conversion to express the data of the object

### task_manager.py
TaskManager has two attributes: tasks is a list contaning objects of Task class and flask app for the API
The constructor sets the attributes to the constructor parameters calls register_routes method to start the API (we will cover that a little later)

TaskManager has add_task() method which appends the task to my list of tasks, however if the type of the parameter is not Task it would return an error message
Example: task_manager.add_task(task)
TaskManager has list_tasks() method which loads all the tasks in my task_manager object
Example: task_manager.list_tasks() would load all the tasks in my list saved in the database, it would output nothing if the database does not contain any of the tasks in the list
TaskManager has save_task() method which saves all the tasks in the list to the database.
Example: task_manager.save_task()
TaskManager has delete_task(id) which looks for a task with the same id and deletes from both the list and the database and returns if it was successful or the if the ID was not found
Example: task_manager.delete_task(id) would return f"Task id: {id} was deleted successfully" if the operation was successful or f"Task id: {id} not found" if it was not

![API-Documentation]:
Here is where we use the register_routes() method which it handles all the flask application calls, Example usage will be provided later on.
Calling the application with the decorator '/tasks' and method GET would result in loading all the tasks according to the URL variable given type 
Calling the application with the decorator '/tasks/<int:task_id>' with GET method would return the task with the mentioned id or return an error message if it does not exist.
Calling the application with the decorator '/tasks/<int:task_id>' with DELETE method would delete the task from the database with the mentioned ID
Calling the application with the decorator '/tasks/pending' with GET method would return all the tasks with 'pending' status
Calling the application with the decorator '/tasks/overdue' with GET method would return all the tasks with 'overdue' status
Calling the application with the decorator '/tasks' with POST method would take in a new task
Calling the application with the decorator '/tasks/<int:task_id>' with PUT method would update an existing task if the task_id is the same, if the provided data is wrong it would return an error message

![Database-Schema]:
Short description about the database is that we save the work and personal tasks under the same file in different tables because there are different attributes for each of them.
Work table: Has TASK_ID, TASK_TYPE (which in that case is 'Work'), TITLE, STATUS, DUE_DATE
Personal table: Has TASK_ID, TASK_TYPE(which is 'Personal'), TITLE, STATUS, DUE_DATE, PRIORITY

![Setup-Instructions]:
1. Create a Virtual Environment (Visual Studio Code -> New terminal)
*python3 -m venv venv-api*
2. Activate the Virtual Environment
*source venv-api/bin/activate*
3. Install Necessary Packages
sudo apt-get install sqlite3
*pip install flask*
4. Deactivate virtual environment
*deactivate*

Run the task_manager using the python compiler py './task_manager.py' (Make sure you are in the same directory)
The default port would be 5015 so that is what we will use in out curl prompts


![Example-Usage]:

Starting with creating a task and automatically adding it to the database:
curl -X POST http://127.0.0.1:5015/tasks -H "Content-Type: application/json" -d "{\"type\": \"Personal\",\"title\": \"First task\", \"due_date\": \"2024-12-31\", \"description\": \"Short\", \"priority\": \"medium\"}"
This will return a message: "Personal task added"

To check if it was added we use the '/tasks' decorator:
curl -X GET http://127.0.0.1:5015/tasks
This will output
(1, 'Personal', 'First task', 'pending', '2024-12-31', 'medium')

We try to use the type so:
curl -X GET http://127.0.0.1:5015/tasks?type=Personal
This will output
(1, 'Personal', 'First task', 'pending', '2024-12-31', 'medium')

We try to use the wrong type so:
curl -X GET http://127.0.0.1:5015/tasks?type=Work
This will output an empty string

We can add a Work task so we can compare:
curl -X POST http://127.0.0.1:5015/tasks -H "Content-Type: application/json" -d "{\"type\": \"Work\",\"title\": \"Second task\", \"due_date\": \"2024-12-31\", \"description\": \"Short\"}"
This will return a message: "Work task added"

We can add a new task with wrong data:
curl -X POST http://127.0.0.1:5015/tasks -H "Content-Type: application/json" -d "{\"type\": \"Not Personal\",\"title\": \"Second task\", \"due_date\": \"2024-12-31\", \"description\": \"Short\"}"
This will return an  "error": "Wrong type of task"

We can check again if it was added we use the '/tasks' decorator:
curl -X GET http://127.0.0.1:5015/tasks
This will output
(1, 'Personal', 'First task', 'pending', '2024-12-31', 'medium')
(2, 'Work', 'Second task', 'pending', '2024-12-31')

We try to use the Personal type so:
curl -X GET http://127.0.0.1:5015/tasks?type=Personal
This will output
(1, 'Personal', 'First task', 'pending', '2024-12-31', 'medium')

We try to use the Work type so:
curl -X GET http://127.0.0.1:5015/tasks?type=Work
This will output 
(2, 'Work', 'Second task', 'pending', '2024-12-31')

We try to delete the Personal task:
curl -X DELETE http://127.0.0.1:5015/tasks/1
The out put will be 
Task id: 1 was deleted successfully

We try to delete with a wrong ID:
curl -X DELETE http://127.0.0.1:5015/tasks/7
The out put will be 
Task id: 7 not found
We can check again if it was deleted we use the '/tasks' decorator:
curl -X GET http://127.0.0.1:5015/tasks
This will output
(2, 'Work', 'Second task', 'pending', '2024-12-31')

If we try to run the delete method again this will output:
Task id: 1 not found

Retrieving tasks using TaskID:
curl -X GET http://127.0.0.1:5015/tasks/2
will output 
(2, 'Work', 'Second task', 'pending', '2024-12-31')
and
curl -X GET http://127.0.0.1:5015/tasks/3
will ouput
Task id: 3 not found

We can add a new Personal task:
curl -X POST http://127.0.0.1:5015/tasks -H "Content-Type: application/json" -d "{\"type\": \"Personal\",\"title\": \"Third task\", \"due_date\": \"2024-12-31\", \"description\": \"Short\",\"priority\": \"low\"}"

New database would be:
curl -X GET http://127.0.0.1:5015/tasks
(2, 'Work', 'Second task', 'pending', '2024-12-31')
(3, 'Personal', 'Third task', 'pending', '2024-12-31', 'low')
Finally updating, We will use the put method to update our Personal task from pending to completed:
curl -X PUT http://127.0.0.1:5015/tasks/3 -H "Content-Type: application/json" -d "{\"status\": \"completed\"}"

We check the status of it
curl -X GET http://127.0.0.1:5015/tasks/3
(3, 'Personal', 'Third task', 'completed', '2024-12-07', 'low')

