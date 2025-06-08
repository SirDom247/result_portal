from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .models import Course, Registration, Result
from .serializers import CourseSerializer, RegistrationSerializer, ResultSerializer
from .utils.excel_parser import process_excel
from .utils.email_sender import send_result_upload_notification

# Course List & Create
class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

# Student Course Registration
class RegisterCourseAPIView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

# View Results (Only for the logged-in student)
class ResultListAPIView(generics.ListAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(student__user=self.request.user)

# Upload Excel Results (Exam Officer/Staff)
class UploadResultView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file temporarily
        file_path = default_storage.save(f'temp/{file_obj.name}', file_obj)
        full_path = default_storage.path(file_path)

        try:
            processed_results = process_excel(full_path)
            send_result_upload_notification(
                email='dominicudousoro@live.com',
                subject='Result Upload Complete',
                message=f'{len(processed_results)} results processed successfully.'
            )
            return Response({'message': f'{len(processed_results)} results processed.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


