#!/usr/bin/env python3
"""
Unit tests for todo.py  (Lab 4 / Lecture 4 - Activity 4: todo-test.py)

Run:  python3 .github/scripts/todo-test.py

Section 1: the test cases (unittest.TestCase)
Section 2: a runner that prints a clean, user-friendly report:

    test_add_task ... ok
    test_get_done_tasks ... ok
    ...
    Total Tests: 5
    Passed: 5 (100.00%)
    Failed: 0 (0.00%)

Change vs. the slides: the slides' runner always exits with code 0 and only
prints lines that contain "ok", so a FAILING test was silently hidden and the
CI pipeline still showed green. This version reports FAIL/ERROR lines, prints
the details, and exits with code 1 when anything fails, so CI goes red.
"""
import sys
import unittest
from io import StringIO

from todo import Task, TaskPool  # works because this script sits next to todo.py


# --------------------------------------------------------------------------- #
# Section 1: test cases
# --------------------------------------------------------------------------- #
class TestTaskPool(unittest.TestCase):

    # Runs before EACH test: a fresh, empty pool every time
    def setUp(self):
        self.pool = TaskPool()

    def test_add_task(self):
        task = Task("New Task")
        self.pool.add_task(task)
        self.assertEqual(len(self.pool.tasks), 1)

    def test_get_open_tasks(self):
        self.pool.populate()
        open_tasks = self.pool.get_open_tasks()
        # Lab 4 PR exercise: if you add a "ToDo" task in todo.py, change 3 -> 4 here.
        self.assertEqual(len(open_tasks), 4)
        self.assertTrue(all(task.status == "ToDo" for task in open_tasks))

    def test_get_done_tasks(self):
        self.pool.populate()
        done_tasks = self.pool.get_done_tasks()
        self.assertEqual(len(done_tasks), 3)
        self.assertTrue(all(task.status == "Done" for task in done_tasks))

    # Extra tests (not in the slides)
    def test_mark_completed(self):
        task = Task("Write report")
        task.mark_completed()
        self.assertTrue(task.completed)
        self.assertEqual(task.status, "Done")

    def test_task_created_as_done_is_completed(self):
        # Covers the small consistency fix in Task.__init__
        self.assertTrue(Task("Already finished", status="Done").completed)
        self.assertFalse(Task("Not started").completed)


# --------------------------------------------------------------------------- #
# Section 2: friendly runner
# --------------------------------------------------------------------------- #
def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskPool)
    # Remember the test ids NOW: a TestSuite forgets its tests after it has run them.
    test_ids = [test.id() for test in suite]

    # Run tests with verbosity 2, capturing unittest's own output in memory
    captured_output = StringIO()
    result = unittest.TextTestRunner(stream=captured_output, verbosity=2).run(suite)

    # Status of every test, taken from the result object (not by searching text for "ok")
    failed_ids = {test.id() for test, _ in result.failures}
    error_ids = {test.id() for test, _ in result.errors}
    skipped_ids = {test.id() for test, _ in result.skipped}

    for test_id in test_ids:
        name = test_id.split(".")[-1]            # keep only the method name
        if test_id in failed_ids:
            status = "FAIL"
        elif test_id in error_ids:
            status = "ERROR"
        elif test_id in skipped_ids:
            status = "skipped"
        else:
            status = "ok"
        print(f"{name} ... {status}")

    # Print total, passed, and failed summary
    total_tests = result.testsRun
    failed_count = len(result.failures) + len(result.errors)
    passed_count = total_tests - failed_count - len(result.skipped)

    def pct(count):
        return (count / total_tests * 100) if total_tests else 0.0

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_count} ({pct(passed_count):.2f}%)")
    print(f"Failed: {failed_count} ({pct(failed_count):.2f}%)")

    # Show WHY something failed (the slides hid this)
    for test, trace in result.failures + result.errors:
        print("\n" + "=" * 60)
        print(f"Details for {test.id().split('.')[-1]}:")
        print(trace.strip())

    return result.wasSuccessful()


if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
