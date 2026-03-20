from django.contrib import admin
from .models import Course, Department, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'credits', 'semester', 'year', 'is_active', 'enrolled_count')
    list_filter = ('semester', 'year', 'department', 'is_active')
    search_fields = ('title', 'code', 'instructor')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_at')
    list_filter = ('status',)
