"""
Unit Tests — Model Layer
Tests the core business logic of Course and Enrollment models.
Risk: HIGH — incorrect model logic breaks enrollment, seat counting, and status transitions.
"""
import pytest
from django.contrib.auth.models import User
from courses.models import Department, Course, Enrollment


@pytest.mark.django_db
class TestCourseModel:

    def test_course_str(self, course):
        assert str(course) == 'CS-T01 - Test Course'

    def test_enrolled_count_zero_initially(self, course):
        assert course.enrolled_count == 0

    def test_enrolled_count_increments_on_enrollment(self, course, student):
        Enrollment.objects.create(student=student, course=course, status='enrolled')
        assert course.enrolled_count == 1

    def test_dropped_enrollment_not_counted(self, course, student):
        Enrollment.objects.create(student=student, course=course, status='dropped')
        assert course.enrolled_count == 0

    def test_waitlisted_not_counted_as_enrolled(self, course, student):
        Enrollment.objects.create(student=student, course=course, status='waitlisted')
        assert course.enrolled_count == 0

    def test_is_full_false_when_seats_available(self, course):
        assert course.is_full is False

    def test_is_full_true_when_at_capacity(self, full_course):
        assert full_course.is_full is True

    def test_available_seats_decreases_on_enrollment(self, course, student):
        initial = course.available_seats
        Enrollment.objects.create(student=student, course=course, status='enrolled')
        assert course.available_seats == initial - 1

    def test_available_seats_never_negative(self, full_course, another_student):
        # Force-create extra enrollment beyond capacity
        Enrollment.objects.create(student=another_student, course=full_course, status='enrolled')
        # available_seats should return 0, not negative
        assert full_course.available_seats >= 0

    def test_course_code_unique(self, department):
        Course.objects.create(
            title='Dup', code='UNIQUE01', department=department,
            description='x', credits=3, max_students=10,
            semester='Fall', year=2024, instructor='X'
        )
        with pytest.raises(Exception):
            Course.objects.create(
                title='Dup2', code='UNIQUE01', department=department,
                description='x', credits=3, max_students=10,
                semester='Fall', year=2024, instructor='Y'
            )

    def test_course_is_active_by_default(self, department):
        c = Course.objects.create(
            title='New', code='NEW01', department=department,
            description='x', credits=3, max_students=10,
            semester='Fall', year=2024, instructor='X'
        )
        assert c.is_active is True


@pytest.mark.django_db
class TestEnrollmentModel:

    def test_enrollment_str(self, enrollment):
        assert 'teststudent' in str(enrollment)
        assert 'CS-T01' in str(enrollment)
        assert 'enrolled' in str(enrollment)

    def test_default_status_is_enrolled(self, course, student):
        e = Enrollment.objects.create(student=student, course=course)
        assert e.status == 'enrolled'

    def test_duplicate_enrollment_raises(self, course, student):
        Enrollment.objects.create(student=student, course=course)
        with pytest.raises(Exception):
            Enrollment.objects.create(student=student, course=course)

    def test_enrollment_status_can_be_updated(self, enrollment):
        enrollment.status = 'dropped'
        enrollment.save()
        enrollment.refresh_from_db()
        assert enrollment.status == 'dropped'

    def test_valid_status_choices(self, course, student):
        for status in ['enrolled', 'dropped', 'completed', 'waitlisted']:
            e = Enrollment.objects.filter(student=student, course=course).first()
            if e:
                e.status = status
                e.save()
            else:
                e = Enrollment.objects.create(student=student, course=course, status=status)
            assert e.status == status


@pytest.mark.django_db
class TestDepartmentModel:

    def test_department_str(self, department):
        assert str(department) == 'Computer Science'

    def test_department_code_unique(self):
        Department.objects.create(name='Dept A', code='UNIQ')
        with pytest.raises(Exception):
            Department.objects.create(name='Dept B', code='UNIQ')
