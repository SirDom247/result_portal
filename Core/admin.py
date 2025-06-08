from django.contrib import admin
from .models import StudentProfile, Course, Registration, Result

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matric_number', 'department', 'level')
    search_fields = ('matric_number', 'user__username')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'unit')
    search_fields = ('code', 'title')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'registered_on')
    list_filter = ('registered_on',)
    search_fields = ('student__matric_number', 'course__code')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'score', 'grade')
    search_fields = ('student__matric_number', 'course__code')
