import json
import os

class Task:
    def __init__(self, id, title, description='', completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

    def __repr__(self):
        status = "✓" if self.completed else "✗"
        return f"Task(id={self.id}, title={self.title}, description={self.description}, completed={status})"

class TaskManager:
    def __init__(self, user):
        self.user = user
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description=''):
        task_id = len(self.tasks) + 1
        task = Task(task_id, title, description)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Added task: {task}")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            for task in self.tasks:
                print(task)

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
        print(f"Task {task_id} deleted.")

    def mark_task_complete(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                print(f"Task {task_id} marked as completed.")
                return
        print(f"Task {task_id} not found.")

    def edit_task(self, task_id, new_title=None, new_description=None):
        for task in self.tasks:
            if task.id == task_id:
                if new_title:
                    task.title = new_title
                if new_description:
                    task.description = new_description
                self.save_tasks()
                print(f"Task {task_id} updated: {task}")
                return
        print(f"Task {task_id} not found.")

    def save_tasks(self):
        with open(f"{self.user}_tasks.json", "w") as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def load_tasks(self):
        try:
            with open(f"{self.user}_tasks.json", "r") as file:
                task_data = json.load(file)
                self.tasks = [Task(**data) for data in task_data]
        except FileNotFoundError:
            self.tasks = []

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def register():
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        # Check if the user already exists
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                users = json.load(file)
                if username in users:
                    print("Username already exists. Please try logging in.")
                    return None
        else:
            users = {}

        users[username] = password

        # Save user data
        with open("users.json", "w") as file:
            json.dump(users, file)
        print(f"User {username} registered successfully.")
        return User(username, password)

    @staticmethod
    def login():
        if not os.path.exists("users.json"):
            print("No users registered yet. Please register first.")
            return None

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Load user data
        with open("users.json", "r") as file:
            users = json.load(file)

        if username in users and users[username] == password:
            print(f"User {username} logged in successfully.")
            return User(username, password)
        else:
            print("Invalid credentials. Please try again.")
            return None

def main():
    print("Welcome to Task Manager")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    user = None

    if choice == "1":
        user = User.register()
    elif choice == "2":
        user = User.login()
    elif choice == "3":
        return
    else:
        print("Invalid choice.")
        return

    if user:
        task_manager = TaskManager(user.username)

        while True:
            print("\nTask Manager")
            print("1. Add a task")
            print("2. View tasks")
            print("3. Delete a task")
            print("4. Mark task as complete")
            print("5. Edit a task")
            print("6. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                title = input("Enter task title: ")
                description = input("Enter task description (optional): ")
                task_manager.add_task(title, description)
            elif choice == "2":
                task_manager.view_tasks()
            elif choice == "3":
                task_id = int(input("Enter task ID to delete: "))
                task_manager.delete_task(task_id)
            elif choice == "4":
                task_id = int(input("Enter task ID to mark as complete: "))
                task_manager.mark_task_complete(task_id)
            elif choice == "5":
                task_id = int(input("Enter task ID to edit: "))
                new_title = input("Enter new title (press Enter to skip): ")
                new_description = input("Enter new description (press Enter to skip): ")
                task_manager.edit_task(task_id, new_title if new_title else None, new_description if new_description else None)
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
