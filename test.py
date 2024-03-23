import unittest
from datetime import datetime
from tasks.priority import Priority
from tasks.task import Task

class TestTask(unittest.TestCase):
    def setUp(self):
        self.date = datetime.now().timestamp()
        self.just_task = Task("test@example.com", "Test task", True, self.date, Priority("High"), self.date)
        self.other_task = Task("not_email", "", False, self.date, Priority("Medium"), self.date)

    def test_init(self):
        self.verify_task(self.just_task, "test@example.com", "Test task", True, "High")
        self.verify_task(self.other_task, "not_email", "", False, "Medium")

    def verify_task(self, task, email, description, complete, priority):
        self.assertEqual(task.creator_email, email)
        self.assertEqual(task.description, description)
        self.assertEqual(task.complete, complete)
        self.assertIsInstance(task.priority, Priority)
        self.assertEqual(str(task.priority), priority)

    def test_pretty_tuple(self):
        self.verify_pretty_tuple(self.just_task, "Test task", "True", "High")
        self.verify_pretty_tuple(self.other_task, "", "False", "Medium")

    def verify_pretty_tuple(self, task, description, complete, priority):
        pretty_tuple = task.pretty_tuple()
        self.assertEqual(pretty_tuple[0], description)
        self.assertEqual(pretty_tuple[1], complete)
        self.assertEqual(pretty_tuple[3], priority)

    def test_mark_complete(self):
        self.just_task.mark_complete()
        self.assertTrue(self.just_task.complete)


class TestPriority(unittest.TestCase):
    def setUp(self):
        self.low = Priority("Low")
        self.medium = Priority("Medium")
        self.high = Priority("High")

    def test_init(self):
        self.assertEqual(str(self.low), "Low")
        self.assertEqual(str(self.medium), "Medium")
        self.assertEqual(str(self.high), "High")

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            Priority("Invalid")
        with self.assertRaises(ValueError):
            Priority(5)

    def test_comparison(self):
        self.assertTrue(self.low < self.medium)
        self.assertTrue(self.medium < self.high)
        self.assertTrue(self.low < self.high)
        self.assertFalse(self.high < self.medium)
        self.assertFalse(self.medium < self.low)
        self.assertFalse(self.high < self.low)

        self.assertTrue(self.low <= self.medium)
        self.assertTrue(self.medium <= self.high)
        self.assertTrue(self.low <= self.high)
        self.assertFalse(self.high <= self.medium)
        self.assertFalse(self.medium <= self.low)
        self.assertFalse(self.high <= self.low)

    def test_equality(self):
        self.assertEqual(self.low, Priority("Low"))
        self.assertEqual(self.medium, Priority("Medium"))
        self.assertEqual(self.high, Priority("High"))

if __name__ == '__main__':
    unittest.main()