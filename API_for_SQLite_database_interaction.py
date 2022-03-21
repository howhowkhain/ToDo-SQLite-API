"""
ToDo API

An API for interacting with different tasks from a database built using SQLite.

1. Show Tasks 
2. Add Task 
3. Change Priority 
4. Delete Task
5. Exit


"""


import sqlite3


# class used to create and initiate our Todo App
class Todo():
    # creates a database file if not exists already
    # enables database file to accept SQL queries
    def __init__(self):
        self.database = sqlite3.connect(
            "SQLite/todo_database.db")
        self.cursor = self.database.cursor()
        self.create_tabel()

    # creates a Todo tasks list named "tasks"
    def create_tabel(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks_table (id INTEGER PRIMARY KEY, name TEXT NOT NULL, priority INTEGER NOT NULL);")

    # function for inputing the task name and task priority
    def add_task(self):
        task_name = input("Enter task: ")
        task_name_no_space = task_name.replace(" ", "")
        # protection for task name
        while not task_name_no_space.isalnum():
            if task_name != "":
                print("Task name is not valid. Try again!")
                task_name = input("Enter task: ")
            # if empty string input (no input) it will exit to the main menu
            else:
                self.main()
        # check if the input task name exist in the database
        check_task_name = self.find_task(task_name_no_space)
        # if task name not existing in database will initiate input for task priority
        if check_task_name == None:
            priority = input("Enter priority: ")
            priority_no_space = priority.strip()
            # protection for task priority not to be less than 1
            while not priority_no_space.isdigit() or int(priority_no_space) < 1:
                if priority != "":
                    print("Priority input not valid. Try again!")
                    priority = input("Enter priority: ")
                    priority_no_space = priority.strip()
                # if empty string input (no input) it will exit to the main menu
                else:
                    self.main()
            self.cursor.execute(
                "INSERT INTO tasks_table (name, priority) VALUES (?, ?)", (task_name, int(
                    priority_no_space)))
            # recording/saving the inputs to the tasks table and closing the database file
            self.database.commit()
            self.show_tasks()
        # if task name already in database file it will show all content of the database
        else:
            print("The task already exists in the database. Try a new task!")

    # function for checking if the task name exists or not in the database
    # returns None if task name doesn't exist otherwise returns the task name
    def find_task(self, task_name):
        for row in self.cursor.execute("SELECT * FROM tasks_table"):
            if task_name == row[1]:
                return task_name
        return None

    # function for checking if the task id exist in database
    # returns True if ID exist
    # returns None if ID doesn't exist
    def find_id(self, task_id):
        for row in self.cursor.execute("SELECT * FROM tasks_table"):
            if task_id == row[0]:
                return True
        return None

    # function used to show the entire database
    def show_tasks(self):
        for row in self.cursor.execute("SELECT * FROM tasks_table"):
            print(row)

    # function for updating task priority
    def change_priority(self):
        task_id = input("Input task ID which you want to update: ")
        task_id_no_space = task_id.strip()
        # protectin against empty ID input
        while not task_id_no_space.isdigit():
            if task_id_no_space != "":
                print("Task ID is not valid. Try again!")
                task_id = input("Input task ID which you want to update: ")
                task_id_no_space = task_id.strip()
            # if empty string input (no input) it will exit to the main menu
            else:
                self.main()
        task_id = int(task_id_no_space)
        # checking if the user id exit inside database
        checked_task_id = self.find_id(task_id)
        # chcking if the user ID exist in database or not
        if checked_task_id == True:
            # ask user for new task priority
            priority = input("Enter new priority: ")
            priority_no_space = priority.strip()
            # protection for task priority not to be less than 1
            while not priority_no_space.isdigit() or int(priority_no_space) < 1:
                if priority != "":
                    print("Priority input not valid. Try again!")
                    priority = input("Enter new priority: ")
                    priority_no_space = priority.strip()
                # if empty string input (no input) it will exit to the main menu
                else:
                    self.main()
            self.cursor.execute(
                f"UPDATE tasks_table SET priority=? WHERE id={task_id}", (int(priority_no_space),))
            self.database.commit()
        else:
            print(f"There is no task with the ID: {task_id}")

    # function for deleting a specified task
    def delete_task(self):
        task_id = input("Input task ID which you want to delete: ")
        task_id_no_space = task_id.strip()
        # protectin against empty ID input
        while not task_id_no_space.isdigit():
            if task_id != "":
                print("Task ID is not valid. Try again!")
                task_id = input("Input task ID which you want to delete: ")
                task_id_no_space = task_id.strip()
            # if empty string input (no input) it will exit to the main menu
            else:
                self.main()
        task_id = int(task_id_no_space)
        # check if the input id exist in the database
        checked_task_id = self.find_id(task_id)
        # if the id exist on the database it will be deleted
        if checked_task_id == True:
            self.cursor.execute(
                "DELETE FROM tasks_table WHERE id=?", (task_id,))
            self.database.commit()
        # if the id doesn't exist it will print a message
        else:
            print(f"There is no task with the ID: {task_id}")

    # function which creats the main menu
    def show_menu(self):
        print("+", "-" * 20, "+")
        print("|", "To Do App".center(20), "|")
        print("+", "-" * 20, "+")
        print("MENU")
        print("=" * 4)
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Change Priority")
        print("4. Delete Task")
        print("5. Exit")

    # function which asks for the user choice input
    def read_user_choice(self):
        self.user_option = input("Enter your choice: ")
        self.user_option_no_space = self.user_option.strip()
        # protection for the user choice input
        while not self.user_option_no_space.isdigit() or int(self.user_option_no_space) not in range(1, 6):
            if self.user_option != "":
                print("Your choice is not valid. Enter a number!")
                self.user_option = input("Enter your choice: ")
                self.user_option_no_space = self.user_option.strip()
            # if empty string input (no input) it will exit to the main menu
            else:
                self.main()
        return self.user_option_no_space

    # function which drives all App and creates the App loop
    def main(self):
        while True:
            self.show_menu()
            self.user_option = self.read_user_choice()
            if self.user_option == "1":
                self.show_tasks()
            elif self.user_option == "2":
                self.add_task()
            elif self.user_option == "3":
                self.change_priority()
            elif self.user_option == "4":
                self.delete_task()
            elif self.user_option == "5":
                self.database.close()
                exit("Bye!")


app = Todo()
app.main()
