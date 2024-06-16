import os
import json
from datetime import datetime

class Task:
    def __init__(self, title, priority='medium', due_date=None, completed=False):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            'title': self.title,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data['title'],
            priority=data['priority'],
            due_date=data['due_date'],
            completed=data['completed']
        )

class ToDoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task) for task in tasks_data]
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, title, priority='medium', due_date=None):
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            self.save_tasks()

    def mark_task_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = True
            self.save_tasks()

    def list_tasks(self):
        for i, task in enumerate(self.tasks):
            status = 'Completed' if task.completed else 'Pending'
            due_date = task.due_date if task.due_date else 'No due date'
            print(f"{i + 1}. [{status}] {task.title} (Priority: {task.priority}, Due: {due_date})")

def main():
    todo_list = ToDoList()

    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Mark Task as Completed")
        print("4. List Tasks")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Task Title: ")
            priority = input("Priority (high, medium, low): ")
            due_date = input("Due Date (YYYY-MM-DD) or leave blank: ")
            due_date = due_date if due_date else None
            todo_list.add_task(title, priority, due_date)
        elif choice == '2':
            todo_list.list_tasks()
            task_index = int(input("Task number to remove: ")) - 1
            todo_list.remove_task(task_index)
        elif choice == '3':
            todo_list.list_tasks()
            task_index = int(input("Task number to mark as completed: ")) - 1
            todo_list.mark_task_completed(task_index)
        elif choice == '4':
            todo_list.list_tasks()
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()