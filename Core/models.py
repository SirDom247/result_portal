from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matric_number})"

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    unit = models.PositiveIntegerField()
    level = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=9, default='2024/2025')   
    semester = models.CharField(max_length=10, default='First')

    def __str__(self):
        return f"{self.code} - {self.title}"
 
class Registration(models.Model):
    REGISTRATION_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)
    academic_year = models.CharField(max_length=9, default='2024/2025')  # e.g., "2024/2025"
    semester = models.CharField(max_length=10, default='First')      # e.g., "Harmattan", "Rain"
    status = models.CharField(max_length=10, choices=REGISTRATION_STATUS, default='pending')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} registered for {self.course}"

    def clean(self):
        # Ensure the course matches the student's department and level
        if self.course.department != self.student.department:
            raise ValidationError("Course department doesn't match student department.")
        if self.course.level != self.student.level:
            raise ValidationError("Course level doesn't match student level.")
        if self.course.semester.lower() != self.semester.lower():
            raise ValidationError("Selected semester does not match course semester.")

    def save(self, *args, **kwargs):
        # Run custom validation before saving
        self.full_clean()  # Calls the `clean()` method
        super().save(*args, **kwargs)


class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    is_approved = models.BooleanField(default=False)
    academic_year = models.CharField(max_length=9, default='2024/2025')   
    semester = models.CharField(max_length=10, default='First')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"Result: {self.student} - {self.course} => {self.grade}"