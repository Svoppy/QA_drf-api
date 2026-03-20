from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Department, Course


class Command(BaseCommand):
    help = 'Seed database with sample AITU courses'

    def handle(self, *args, **kwargs):
        # Departments
        depts = [
            ('Computer Science', 'CS'),
            ('Software Engineering', 'SE'),
            ('Cybersecurity', 'CY'),
            ('Data Science', 'DS'),
            ('Information Systems', 'IS'),
        ]
        dept_objs = {}
        for name, code in depts:
            d, _ = Department.objects.get_or_create(code=code, defaults={'name': name})
            dept_objs[code] = d
            self.stdout.write(f'  Department: {name}')

        # Courses
        courses = [
            ('CS101', 'Introduction to Programming', 'CS', 'A foundation course covering Python programming fundamentals, algorithms, and problem-solving techniques.', 5, 40, 'Fall', 2024, 'Dr. Aigerim Bekova'),
            ('CS201', 'Data Structures and Algorithms', 'CS', 'Covers arrays, linked lists, trees, graphs, sorting, and algorithmic complexity.', 5, 35, 'Spring', 2024, 'Prof. Serik Nurgali'),
            ('CS301', 'Operating Systems', 'CS', 'Process management, memory management, file systems, and concurrency.', 5, 30, 'Fall', 2024, 'Dr. Dias Abenov'),
            ('SE101', 'Software Engineering Fundamentals', 'SE', 'SDLC, Agile methodologies, requirements engineering, and project management.', 4, 35, 'Fall', 2024, 'Dr. Aliya Nurlanovna'),
            ('SE201', 'Web Development', 'SE', 'HTML, CSS, JavaScript, Django, REST APIs, and deployment fundamentals.', 4, 40, 'Spring', 2024, 'Prof. Ruslan Seitkali'),
            ('SE301', 'Software Testing and QA', 'SE', 'Test planning, unit testing, integration testing, E2E testing, and CI/CD.', 4, 30, 'Fall', 2024, 'Dr. Meiram Dzhaksybekov'),
            ('CY101', 'Introduction to Cybersecurity', 'CY', 'Security fundamentals, cryptography basics, network security, and threat modeling.', 4, 35, 'Spring', 2024, 'Prof. Zarina Kasymova'),
            ('CY201', 'Network Security', 'CY', 'Firewalls, VPNs, intrusion detection systems, and penetration testing basics.', 4, 25, 'Fall', 2024, 'Dr. Arman Bekzhan'),
            ('DS101', 'Introduction to Data Science', 'DS', 'Python for data analysis, pandas, numpy, visualization, and basic ML concepts.', 5, 40, 'Fall', 2024, 'Dr. Dinara Seitkali'),
            ('DS201', 'Machine Learning', 'DS', 'Supervised and unsupervised learning, model evaluation, and scikit-learn.', 5, 30, 'Spring', 2024, 'Prof. Bakyt Nurpeisov'),
            ('IS101', 'Database Management Systems', 'IS', 'Relational databases, SQL, normalization, transactions, and PostgreSQL.', 4, 40, 'Fall', 2024, 'Dr. Gulnar Akhmetova'),
            ('IS201', 'Enterprise Systems', 'IS', 'ERP systems, business process management, and system integration.', 4, 30, 'Spring', 2024, 'Prof. Askar Dzhubanov'),
        ]

        for code, title, dept_code, desc, credits, max_s, sem, year, instructor in courses:
            c, created = Course.objects.get_or_create(
                code=code,
                defaults={
                    'title': title,
                    'department': dept_objs[dept_code],
                    'description': desc,
                    'credits': credits,
                    'max_students': max_s,
                    'semester': sem,
                    'year': year,
                    'instructor': instructor,
                }
            )
            self.stdout.write(f'  {"Created" if created else "Exists"}: {code} - {title}')

        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@aitu.edu.kz', 'admin1234')
            self.stdout.write('  Created superuser: admin / admin1234')

        # Sample student
        if not User.objects.filter(username='student1').exists():
            User.objects.create_user('student1', 'student1@aitu.edu.kz', 'Student1234!',
                                     first_name='Aizat', last_name='Bekova')
            self.stdout.write('  Created student: student1 / Student1234!')

        self.stdout.write(self.style.SUCCESS('Seed complete.'))
