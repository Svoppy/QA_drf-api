from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Course, Enrollment, Department


def course_list(request):
    courses = Course.objects.filter(is_active=True).select_related('department')

    query = request.GET.get('q', '')
    department_id = request.GET.get('department', '')
    semester = request.GET.get('semester', '')

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(code__icontains=query) |
            Q(instructor__icontains=query)
        )
    if department_id:
        courses = courses.filter(department_id=department_id)
    if semester:
        courses = courses.filter(semester=semester)

    departments = Department.objects.all()
    enrolled_course_ids = set()
    if request.user.is_authenticated:
        enrolled_course_ids = set(
            Enrollment.objects.filter(
                student=request.user, status='enrolled'
            ).values_list('course_id', flat=True)
        )

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'departments': departments,
        'query': query,
        'selected_department': department_id,
        'selected_semester': semester,
        'enrolled_course_ids': enrolled_course_ids,
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, is_active=True)
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(
            student=request.user, course=course
        ).first()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'enrollment': enrollment,
    })


@login_required
def enroll(request, pk):
    course = get_object_or_404(Course, pk=pk, is_active=True)

    if request.method == 'POST':
        existing = Enrollment.objects.filter(student=request.user, course=course).first()
        if existing:
            if existing.status == 'enrolled':
                messages.warning(request, 'You are already enrolled in this course.')
            elif existing.status == 'dropped':
                existing.status = 'enrolled'
                existing.save()
                messages.success(request, f'Re-enrolled in {course.title}.')
        elif course.is_full:
            Enrollment.objects.create(student=request.user, course=course, status='waitlisted')
            messages.info(request, f'Course is full. Added to waitlist for {course.title}.')
        else:
            Enrollment.objects.create(student=request.user, course=course)
            messages.success(request, f'Successfully enrolled in {course.title}.')

    return redirect('course_detail', pk=pk)


@login_required
def drop_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course, status='enrolled')

    if request.method == 'POST':
        enrollment.status = 'dropped'
        enrollment.save()
        messages.success(request, f'Dropped {course.title}.')

    return redirect('course_detail', pk=pk)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course', 'course__department').order_by('-enrolled_at')
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})
