
import unittest
from input_code.gestion_notes import Student

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student("Alice")

    def test_add_grade_valid(self):
        self.student.add_grade(15)
        self.assertIn(15, self.student.grades)

    def test_add_grade_invalid(self):
        with self.assertRaises(ValueError):
            self.student.add_grade(25)  # Note invalide, doit lever une exception

    def test_average_no_grades(self):
        self.assertEqual(self.student.average(), 0)

    def test_average_with_grades(self):
        self.student.add_grade(10)
        self.student.add_grade(15)
        self.assertEqual(self.student.average(), 12.5)

    def test_has_passed_no_grades(self):
        self.assertFalse(self.student.has_passed())

    def test_has_passed_with_passing_grades(self):
        self.student.add_grade(10)
        self.student.add_grade(12)
        self.assertTrue(self.student.has_passed())

    def test_has_passed_with_failing_grades(self):
        self.student.add_grade(8)
        self.student.add_grade(9)
        self.assertFalse(self.student.has_passed())

if __name__ == '__main__':
    unittest.main()
