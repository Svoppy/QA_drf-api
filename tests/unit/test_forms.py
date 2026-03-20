"""
Unit Tests — Form Validation
Tests registration form validation logic.
Risk: HIGH — invalid inputs must be caught at the form level before hitting the DB.
"""
import pytest
from django.contrib.auth.models import User
from users.forms import RegisterForm


@pytest.mark.django_db
class TestRegisterForm:

    def _valid_data(self, **overrides):
        data = {
            'username': 'newstudent',
            'first_name': 'Aizat',
            'last_name': 'Bekova',
            'email': 'aizat@aitu.edu.kz',
            'password1': 'StrongPass1234!',
            'password2': 'StrongPass1234!',
        }
        data.update(overrides)
        return data

    def test_valid_form(self):
        form = RegisterForm(data=self._valid_data())
        assert form.is_valid(), form.errors

    def test_mismatched_passwords_invalid(self):
        form = RegisterForm(data=self._valid_data(password2='WrongPass!'))
        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_duplicate_email_invalid(self, db):
        User.objects.create_user('existing', email='taken@aitu.edu.kz', password='pass')
        form = RegisterForm(data=self._valid_data(email='taken@aitu.edu.kz'))
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_missing_email_invalid(self):
        form = RegisterForm(data=self._valid_data(email=''))
        assert not form.is_valid()

    def test_missing_first_name_invalid(self):
        form = RegisterForm(data=self._valid_data(first_name=''))
        assert not form.is_valid()

    def test_short_password_invalid(self):
        form = RegisterForm(data=self._valid_data(password1='short', password2='short'))
        assert not form.is_valid()

    def test_numeric_only_password_invalid(self):
        form = RegisterForm(data=self._valid_data(password1='12345678', password2='12345678'))
        assert not form.is_valid()

    def test_valid_form_saves_user(self, db):
        form = RegisterForm(data=self._valid_data())
        assert form.is_valid()
        user = form.save()
        assert User.objects.filter(username='newstudent').exists()
        assert user.email == 'aizat@aitu.edu.kz'
