from datetime import datetime,date
from task import *
import csv
import inspect
from flask import Flask,jsonify,request,render_template
class TaskManager:
    def __init__(self,tasks,app):
        self.tasks = tasks
        self.app = app
        self.register_routes()
    def add_task(self,task):
        if type(task) is PersonalTask or WorkTask:
            self.tasks.append(task)
            task.save_to_db()
        else:
            print("Wrong type")
            return "Wrong type"
    def list_tasks(self,flag=None):
        for task in self.tasks:
            task.load_from_db()

    def save_task(self):
        for task in self.tasks:
            task.save_to_db()

    def delete_task(self,id):
        for task in self.tasks:
            if(task.get_task_id() == id):
                self.tasks.remove(task)
                task.delete_from_db()
                return f"Task id: {id} was deleted successfully"
        return f"Task id: {id} not found"

    def register_routes(self):
        @self.app.route('/tasks', methods=["GET"])
        def load_task():
            type = request.args.get('type')
            allTasks =[]
            if not self.tasks:
                return "Not found"
            elif type:
                for task in self.tasks:
                    if task.flag == type:
                        allTasks.append(task.load_from_db())
            else:
                for task in self.tasks:
                    allTasks.append(task.load_from_db())
            return '\n'.join(allTasks)
        @self.app.route('/tasks/<int:task_id>', methods=["GET"])
        def get_task_using_id(task_id):
            for task in self.tasks:
                if task.get_task_id() == task_id:
                    return task.load_from_db()
            return f"Task ID: {task_id} is not found"
        @self.app.route('/tasks/<int:task_id>', methods=["DELETE"])
        def delete_task_from_db(task_id):
            return self.delete_task(task_id)
        @self.app.route('/tasks/pending',methods=["GET"])
        def get_pending_tasks():
            pendingTasks = [f'Task ID: {task.get_task_id()} is pending' for task in self.tasks if task.status == "pending"]
            return '\n'.join(pendingTasks)

        @self.app.route('/tasks/overdue',methods=["GET"])
        def get_overdue_tasks():
            overdue = [f'Task ID: {task.get_task_id()} is overdue' for task in self.tasks if datetime.strptime(task.due_date,'%Y-%m-%d').date() < date.today()]
            return '\n'.join(overdue)
        
        @self.app.route('/tasks', methods=["POST"])
        def put_task():
            new_task = request.json

            if new_task["type"] == "Personal":
                if "title" in new_task and "due_date" in new_task and "priority" in new_task:
                    task_title = new_task["title"]
                    task_date = new_task["due_date"]
                    task = PersonalTask(task_title,task_date)
                    task.set_description(new_task["description"])
                    task.set_priority(new_task["priority"])
                    self.add_task(task)
                    return jsonify({"message": "Personal task added"}), 201
                else:
                    return jsonify({"message": "Input data was wrong"}), 404
            elif new_task['type'] == 'Work':
                if "title" in new_task and "due_date" in new_task:
                    task_title = new_task["title"]
                    task_date = new_task["due_date"]
                    task = WorkTask(task_title,task_date)
                    task.set_description(new_task["description"])
                    self.add_task(task)
                    return jsonify({"message": "Work task added"}), 201
                else:
                    return jsonify({"message": "Input data was wrong"}), 404

            else:
                return jsonify({"error": "Wrong type of task"}), 404
        @self.app.route('/tasks/<int:task_id>', methods=["PUT"])
        def update_task(task_id):
            updated_task = request.json
            final_task = None
            for task in self.tasks:
                if task.get_task_id() == task_id:
                    final_task = task
                    break
            if final_task:
                if final_task.flag == "Personal":
                    if "priority" in updated_task:
                        final_task.set_priority(updated_task["priority"])
                    if "status" in updated_task:
                        if updated_task["status"] == "completed":
                            final_task.mark_completed()
                        else:
                            final_task.status = 'pending'
                    if "description" in updated_task:
                        final_task.description = updated_task["description"]
                elif final_task.flag == "Work":
                    if updated_task["description"]:
                        final_task.description = updated_task["description"]
                final_task.update_in_db()
                return f"Task ID: {task_id} has been updated!"
            else:
                return f"Data inserted was wrong"
            return f"Task ID: {task_id} does not exist"
            
if __name__ == "__main__":
    app = Flask(__name__)
    task_manager = TaskManager([],app)
    
    task_manager.app.run(debug=True, port=5015)
