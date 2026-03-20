import os
import sys
import django
import pytest

# Support running from repo root (local) or from /app (Docker)
_here = os.path.dirname(__file__)
_app_dir = os.path.join(_here, '..', 'app')
if os.path.isdir(_app_dir):
    sys.path.insert(0, os.path.abspath(_app_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Department, Course, Enrollment


@pytest.fixture
def department(db):
    return Department.objects.create(name='Computer Science', code='CS-TEST')


@pytest.fixture
def course(db, department):
    return Course.objects.create(
        title='Test Course',
        code='CS-T01',
        department=department,
        description='A test course for QA purposes.',
        credits=4,
        max_students=5,
        semester='Fall',
        year=2024,
        instructor='Dr. Test',
    )


@pytest.fixture
def full_course(db, department):
    c = Course.objects.create(
        title='Full Course',
        code='CS-T02',
        department=department,
        description='A full course.',
        credits=3,
        max_students=1,
        semester='Spring',
        year=2024,
        instructor='Dr. Full',
    )
    student = User.objects.create_user('filler_student', password='pass123')
    Enrollment.objects.create(student=student, course=c, status='enrolled')
    return c


@pytest.fixture
def student(db):
    return User.objects.create_user(
        username='teststudent',
        email='test@aitu.edu.kz',
        password='TestPass1234!',
        first_name='Test',
        last_name='Student',
    )


@pytest.fixture
def another_student(db):
    return User.objects.create_user(
        username='student2',
        email='student2@aitu.edu.kz',
        password='TestPass1234!',
    )


@pytest.fixture
def enrollment(db, student, course):
    return Enrollment.objects.create(student=student, course=course, status='enrolled')


@pytest.fixture
def client(db):
    from django.test import Client
    return Client()


@pytest.fixture
def auth_client(db, student):
    from django.test import Client
    c = Client()
    c.login(username='teststudent', password='TestPass1234!')
    return c
