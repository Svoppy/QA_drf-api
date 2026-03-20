"""
Integration Tests — View Layer
Tests HTTP request/response cycles, auth flows, and enrollment workflows.
Risk: HIGH — these cover the primary user journeys and access control.
"""
import pytest
from django.urls import reverse
from courses.models import Enrollment


@pytest.mark.django_db
class TestAuthViews:

    def test_login_page_accessible(self, client):
        response = client.get('/users/login/')
        assert response.status_code == 200

    def test_register_page_accessible(self, client):
        response = client.get('/users/register/')
        assert response.status_code == 200

    def test_login_valid_credentials(self, client, student):
        response = client.post('/users/login/', {
            'username': 'teststudent',
            'password': 'TestPass1234!',
        })
        assert response.status_code == 302
        assert response.url == '/courses/'

    def test_login_invalid_credentials(self, client, student):
        response = client.post('/users/login/', {
            'username': 'teststudent',
            'password': 'wrongpassword',
        })
        assert response.status_code == 200
        assert b'Invalid' in response.content

    def test_register_creates_user_and_logs_in(self, client, db):
        response = client.post('/users/register/', {
            'username': 'brandnew',
            'first_name': 'Brand',
            'last_name': 'New',
            'email': 'brandnew@aitu.edu.kz',
            'password1': 'StrongPass1234!',
            'password2': 'StrongPass1234!',
        })
        assert response.status_code == 302
        from django.contrib.auth.models import User
        assert User.objects.filter(username='brandnew').exists()

    def test_profile_requires_login(self, client):
        response = client.get('/users/profile/')
        assert response.status_code == 302
        assert '/users/login/' in response.url

    def test_profile_accessible_when_authenticated(self, auth_client):
        response = auth_client.get('/users/profile/')
        assert response.status_code == 200

    def test_logout_redirects_to_login(self, auth_client):
        response = auth_client.post('/users/logout/')
        assert response.status_code == 302


@pytest.mark.django_db
class TestCourseListView:

    def test_course_list_accessible_without_login(self, client, course):
        response = client.get('/courses/')
        assert response.status_code == 200

    def test_course_list_shows_active_courses(self, client, course):
        response = client.get('/courses/')
        assert course.title.encode() in response.content

    def test_search_by_title(self, client, course):
        response = client.get('/courses/?q=Test+Course')
        assert response.status_code == 200
        assert b'Test Course' in response.content

    def test_search_no_results(self, client, course):
        response = client.get('/courses/?q=zzznomatch')
        assert response.status_code == 200
        assert b'Test Course' not in response.content

    def test_filter_by_semester(self, client, course):
        response = client.get('/courses/?semester=Fall')
        assert response.status_code == 200

    def test_inactive_course_not_shown(self, client, course):
        course.is_active = False
        course.save()
        response = client.get('/courses/')
        assert b'Test Course' not in response.content


@pytest.mark.django_db
class TestCourseDetailView:

    def test_course_detail_accessible(self, client, course):
        response = client.get(f'/courses/{course.pk}/')
        assert response.status_code == 200
        assert course.title.encode() in response.content

    def test_course_detail_404_for_inactive(self, client, course):
        course.is_active = False
        course.save()
        response = client.get(f'/courses/{course.pk}/')
        assert response.status_code == 404

    def test_enroll_button_visible_for_authenticated(self, auth_client, course):
        response = auth_client.get(f'/courses/{course.pk}/')
        assert b'Enroll' in response.content

    def test_login_prompt_for_unauthenticated(self, client, course):
        response = client.get(f'/courses/{course.pk}/')
        assert b'log in' in response.content


@pytest.mark.django_db
class TestEnrollmentWorkflow:

    def test_enroll_success(self, auth_client, course):
        response = auth_client.post(f'/courses/{course.pk}/enroll/')
        assert response.status_code == 302
        assert Enrollment.objects.filter(course=course, status='enrolled').exists()

    def test_enroll_requires_login(self, client, course):
        response = client.post(f'/courses/{course.pk}/enroll/')
        assert response.status_code == 302
        assert '/users/login/' in response.url

    def test_enroll_full_course_creates_waitlist(self, auth_client, full_course):
        response = auth_client.post(f'/courses/{full_course.pk}/enroll/')
        assert response.status_code == 302
        assert Enrollment.objects.filter(course=full_course, status='waitlisted').exists()

    def test_double_enroll_no_duplicate(self, auth_client, course, enrollment):
        auth_client.post(f'/courses/{course.pk}/enroll/')
        count = Enrollment.objects.filter(course=course, status='enrolled').count()
        assert count == 1

    def test_drop_course_success(self, auth_client, course, enrollment):
        response = auth_client.post(f'/courses/{course.pk}/drop/')
        assert response.status_code == 302
        enrollment.refresh_from_db()
        assert enrollment.status == 'dropped'

    def test_drop_requires_login(self, client, course, enrollment):
        response = client.post(f'/courses/{course.pk}/drop/')
        assert response.status_code == 302
        assert '/users/login/' in response.url

    def test_my_courses_shows_enrollments(self, auth_client, enrollment):
        response = auth_client.get('/courses/my/')
        assert response.status_code == 200
        assert b'Test Course' in response.content

    def test_reenroll_after_drop(self, auth_client, course, enrollment):
        # Drop first
        auth_client.post(f'/courses/{course.pk}/drop/')
        enrollment.refresh_from_db()
        assert enrollment.status == 'dropped'
        # Re-enroll
        auth_client.post(f'/courses/{course.pk}/enroll/')
        enrollment.refresh_from_db()
        assert enrollment.status == 'enrolled'
