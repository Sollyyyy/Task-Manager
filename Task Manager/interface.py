from task import *
from task_manager import *
from datetime import datetime

def display_menu():
    print("\nTask Manager")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. List Tasks")
    print("4. View pending and overdue tasks")
    print("5. Save the task list into the csv file")
    print("6. Load the task list from the csv file")
    print("0. Exit")
def main():
    task_manager = TaskManager([],'task_list.csv')
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            task_type = input("1.Personal and 2.Work: ")
            if task_type == '1':
                task_name = input("Enter task name: ")
                due_date = datetime.strptime(input("Enter due date (YYYY-MM-DD): "),'%Y-%m-%d').date()
                task = PersonalTask(task_name,due_date)
                priority = input("Set priority (high, medium, low): ")
                task.set_priority(priority)
                task_manager.add_task(task)
            elif task_type == '2':
                task_name = input("Enter task name: ")
                due_date = datetime.strptime(input("Enter due date (YYYY-MM-DD): "),'%Y-%m-%d').date()
                task = WorkTask(task_name,due_date)
                while True:
                    print("Press 0 to exit")
                    print("Press 1 to add a member to your team")
                    new_choice = int(input())
                    if new_choice == 0:
                        task_manager.add_task(task)
                        break
                    elif new_choice == 1:
                        member=input("Insert team member name: ")
                        task.add_team_member(member)
                    
        elif choice == '2':
            task_id = int(input("Enter task ID to remove: "))
            task_manager.delete_task(task_id)
        elif choice =='3':
            print("To view all tasks press 1 to filter it press 2")
            newestchoice = int(input())
            if newestchoice == 1:
                task_manager.list_tasks()
            elif newestchoice == 2:
                flag = input("Personal or Work related: ")
                task_manager.list_tasks(flag)
        elif choice =='4':
            print(task_manager.get_pending_tasks())
            print(task_manager.get_overdue_tasks())
        elif choice =='5':
            task_manager.save_task()
        elif choice=='6':
            print("Load")
        elif choice=='0':
            print("Exiting")
            break
if __name__ == "__main__":
    main()
                