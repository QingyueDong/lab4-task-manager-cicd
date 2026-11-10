#!/usr/bin/env python3
"""
Task manager  (Lab 4 / Lecture 4 - Activity 3: todo.py)

Section 1: Task      - one task with a title and a status ("ToDo" or "Done")
Section 2: TaskPool  - a collection of tasks with filters for open / done tasks
Section 3: main()    - builds a sample pool and prints the "ToDo Tasks:" and
                       "Done Tasks:" lists. update_index.sh reads this output,
                       so keep those two heading lines exactly as they are.
"""


# --------------------------------------------------------------------------- #
# Section 1: Task
# --------------------------------------------------------------------------- #
class Task:
    # Constructor initializes the task with title and status
    def __init__(self, title, status="ToDo"):
        self.title = title
        self.status = status  # Status defaults to "ToDo"
        # Small fix vs. the slides: the slides always set completed = False, so
        # Task("x", status="Done") was "Done" but not completed. Keep them consistent.
        self.completed = status == "Done"

    # Marks the task as completed and changes its status to "Done"
    def mark_completed(self):
        self.completed = True
        self.status = "Done"

    # Returns a string representation of the task for easier viewing in collections
    def __repr__(self):
        return f"{self.title} - {'Done' if self.completed else 'ToDo'}"

    # Returns a human-readable string representation of the task
    def __str__(self):
        return f"Task: {self.title}, Status: {self.status}"


# --------------------------------------------------------------------------- #
# Section 2: TaskPool
# --------------------------------------------------------------------------- #
class TaskPool:
    # Initializes an empty task pool
    def __init__(self):
        self.tasks = []

    # Populates the task pool with sample tasks of different statuses
    def populate(self):
        task1 = Task("Add Login UI", status="Done")
        task2 = Task("Fix UI Bug", status="Done")
        task3 = Task("Write Tests", status="Done")
        task4 = Task("Update Login UI", status="ToDo")
        task5 = Task("Update Documentation", status="ToDo")
        task6 = Task("Deploy to Production", status="ToDo")
        # Lab 4 Activity 10 (PR exercise): add a new task here, e.g.
        # task7 = Task("Configure CI pipeline", status="ToDo")
        task7 = Task("Configure CI pipeline", status="ToDo")
        # ...then add it to the list below AND update the expected count in todo-test.py.

        task1.mark_completed()
        task2.mark_completed()
        task3.mark_completed()

        self.tasks = [task1, task2, task3, task4, task5, task6, task7]

    # Adds a Task object to the pool
    def add_task(self, task):
        self.tasks.append(task)

    # Returns the tasks whose status is "ToDo"
    def get_open_tasks(self):
        return [task for task in self.tasks if task.status == "ToDo"]

    # Returns the tasks whose status is "Done"
    def get_done_tasks(self):
        return [task for task in self.tasks if task.status == "Done"]


# --------------------------------------------------------------------------- #
# Section 3: main
# --------------------------------------------------------------------------- #
def main():
    pool = TaskPool()
    pool.populate()

    task_titles = [task.title for task in pool.get_open_tasks()]
    print("ToDo Tasks:")
    for title in task_titles:
        print(title)

    completed_titles = [task.title for task in pool.get_done_tasks()]
    print("\nDone Tasks:")
    for title in completed_titles:
        print(title)


if __name__ == "__main__":
    main()
