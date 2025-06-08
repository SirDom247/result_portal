from django.urls import path
from . import views
from .views import UploadResultView

urlpatterns = [
    path('courses/', views.CourseListCreateAPIView.as_view(), name='courses'),
    path('register/', views.RegisterCourseAPIView.as_view(), name='register-course'),
    path('results/', views.ResultListAPIView.as_view(), name='results'),
    path('upload-results/', UploadResultView.as_view(), name='upload-results'),
]