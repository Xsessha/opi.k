import unittest

from enroll import (
    AlreadyEnrolledError,
    CourseFullError,
    CourseNotFoundError,
    CourseSystem,
    NotRegisteredStudentError,
)


class TestEnrollStudentFormalSpecification(unittest.TestCase):
    def setUp(self):
        self.system = CourseSystem()
        for student_id in ("S1", "S2", "S3", "S4"):
            self.system.add_student(student_id)

        self.system.add_course("C1", 2)
        self.system.add_course("C2", 2)
        self.system.add_course("C3", 1)

    def assert_state_unchanged_after_error(self, expected_error, student_id, course_id):
        before = self.system.snapshot()

        with self.assertRaises(expected_error):
            self.system.enroll_student(student_id, course_id)

        self.assertEqual(before, self.system.snapshot())
        self.assertTrue(self.system.check_invariants())

    def test_positive_registered_student_can_enroll_in_existing_course(self):
        self.assertTrue(self.system.enroll_student("S1", "C1"))

        self.assertTrue(self.system.is_enrolled("S1", "C1"))
        self.assertEqual(1, self.system.available_seats("C1"))
        self.assertTrue(self.system.check_invariants())

    def test_positive_multiple_students_can_fill_course_without_exceeding_capacity(self):
        self.assertTrue(self.system.enroll_student("S2", "C2"))
        self.assertTrue(self.system.enroll_student("S3", "C2"))

        self.assertTrue(self.system.is_enrolled("S2", "C2"))
        self.assertTrue(self.system.is_enrolled("S3", "C2"))
        self.assertEqual(0, self.system.available_seats("C2"))
        self.assertTrue(self.system.check_invariants())

    def test_positive_one_student_can_enroll_in_different_courses(self):
        self.assertTrue(self.system.enroll_student("S4", "C1"))
        self.assertTrue(self.system.enroll_student("S4", "C3"))

        self.assertTrue(self.system.is_enrolled("S4", "C1"))
        self.assertTrue(self.system.is_enrolled("S4", "C3"))
        self.assertEqual(1, self.system.available_seats("C1"))
        self.assertEqual(0, self.system.available_seats("C3"))
        self.assertTrue(self.system.check_invariants())

    def test_negative_unregistered_student_is_rejected(self):
        self.assert_state_unchanged_after_error(NotRegisteredStudentError, "Sx", "C1")

    def test_negative_unknown_course_is_rejected(self):
        self.assert_state_unchanged_after_error(CourseNotFoundError, "S1", "Cx")

    def test_negative_duplicate_enrollment_is_rejected(self):
        self.system.enroll_student("S1", "C1")

        self.assert_state_unchanged_after_error(AlreadyEnrolledError, "S1", "C1")

    def test_negative_full_course_is_rejected(self):
        self.system.enroll_student("S4", "C3")

        self.assert_state_unchanged_after_error(CourseFullError, "S2", "C3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
