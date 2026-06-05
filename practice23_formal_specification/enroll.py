class EnrollmentError(Exception):
    """Base class for enrollment operation contract violations."""


class CourseFullError(EnrollmentError):
    pass


class AlreadyEnrolledError(EnrollmentError):
    pass


class NotRegisteredStudentError(EnrollmentError):
    pass


class CourseNotFoundError(EnrollmentError):
    pass


class CourseSystem:
    def __init__(self):
        self.students = set()
        self.courses = {}
        self.enrollments = {}

    @staticmethod
    def _validate_identifier(identifier, field_name):
        if identifier is None:
            raise ValueError(f"{field_name} must not be None")
        if isinstance(identifier, str) and identifier.strip() == "":
            raise ValueError(f"{field_name} must not be empty")
        if not isinstance(identifier, (str, int)):
            raise TypeError(f"{field_name} must be a string or an integer")

    def add_student(self, student_id):
        self._validate_identifier(student_id, "student_id")
        self.students.add(student_id)

    def add_course(self, course_id, capacity):
        self._validate_identifier(course_id, "course_id")
        if not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity < 0:
            raise ValueError("capacity must be non-negative")

        current_enrolled = len(self.enrollments.get(course_id, set()))
        if capacity < current_enrolled:
            raise ValueError("capacity cannot be lower than current enrollments")

        self.courses[course_id] = capacity
        self.enrollments.setdefault(course_id, set())

    def enrolled_count(self, course_id):
        if course_id not in self.courses:
            raise CourseNotFoundError(course_id)
        return len(self.enrollments.get(course_id, set()))

    def available_seats(self, course_id):
        if course_id not in self.courses:
            raise CourseNotFoundError(course_id)
        return self.courses[course_id] - self.enrolled_count(course_id)

    def is_enrolled(self, student_id, course_id):
        return student_id in self.enrollments.get(course_id, set())

    def snapshot(self):
        return (
            set(self.students),
            dict(self.courses),
            {course_id: set(student_ids) for course_id, student_ids in self.enrollments.items()},
        )

    def enroll_student(self, student_id, course_id):
        """Enroll a registered student in an existing course.

        Preconditions:
        - student_id is registered in self.students;
        - course_id exists in self.courses;
        - the student is not already enrolled in the course;
        - the course has at least one available seat.

        Postconditions on success:
        - the pair (student_id, course_id) exists in the enrollment relation;
        - available seats for the selected course decrease by exactly 1;
        - all other courses and students stay unchanged;
        - all state invariants remain true.
        """
        if student_id not in self.students:
            raise NotRegisteredStudentError(student_id)
        if course_id not in self.courses:
            raise CourseNotFoundError(course_id)
        if self.is_enrolled(student_id, course_id):
            raise AlreadyEnrolledError((student_id, course_id))
        if self.available_seats(course_id) <= 0:
            raise CourseFullError(course_id)

        before_students, before_courses, before_enrollments = self.snapshot()
        before_seats = self.available_seats(course_id)
        before_other_seats = {
            other_course_id: self.available_seats(other_course_id)
            for other_course_id in self.courses
            if other_course_id != course_id
        }

        self.enrollments[course_id].add(student_id)

        assert self.is_enrolled(student_id, course_id)
        assert self.available_seats(course_id) == before_seats - 1
        assert self.students == before_students
        assert self.courses == before_courses
        assert self.enrollments[course_id] == before_enrollments[course_id] | {student_id}
        for other_course_id, seats in before_other_seats.items():
            assert self.available_seats(other_course_id) == seats
        assert self.check_invariants()

        return True

    def check_invariants(self):
        for student_id in self.students:
            if student_id is None:
                return False
            if isinstance(student_id, str) and student_id.strip() == "":
                return False

        for course_id, capacity in self.courses.items():
            if course_id is None:
                return False
            if isinstance(course_id, str) and course_id.strip() == "":
                return False
            if not isinstance(capacity, int) or capacity < 0:
                return False

        for course_id, student_ids in self.enrollments.items():
            if course_id not in self.courses:
                return False
            if len(student_ids) > self.courses[course_id]:
                return False
            for student_id in student_ids:
                if student_id not in self.students:
                    return False

        for course_id in self.courses:
            if self.available_seats(course_id) != self.courses[course_id] - self.enrolled_count(course_id):
                return False

        return True
