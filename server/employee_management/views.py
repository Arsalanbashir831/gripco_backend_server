
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import CustomPageNumberPagination
from .serializers import (
    CustomUserRegistrationSerializer,
    CustomUserLoginSerializer,
    CustomUserSerializer,
    DepartmentSerializer,
    BranchSerializer,
    DesignationSerializer,
    ApplicationLeaveSerializer,
    DailyWorkReportsSerializer
)
from .models import CustomUser, Departments, Branches, Designations,DailyWorkReports , ApplicationLeave
from rest_framework.exceptions import PermissionDenied

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "email": user.email,
                    "full_name": user.full_name,
                    "profile_picture": user.profile_picture.url if user.profile_picture else None,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        error_messages = serializer.errors
        formatted_errors = {key: value[0] if isinstance(value, list) else value for key, value in error_messages.items()}
        return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(is_staff=False)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['email', 'full_name', 'branch__branch_name', 'department__department_name', 'designation__designation_name']
    ordering_fields = ['email', 'full_name', 'date_joined']


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branches.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['branch_name', 'branch_location', 'branch_contact', 'branch_email']
    ordering_fields = ['branch_name', 'branch_location', 'branch_created']


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['department_name', 'department_status']
    ordering_fields = ['department_name', 'department_created']


class DesignationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Designations.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['designation_name', 'designation_status']
    ordering_fields = ['designation_name', 'designation_created']




class DailyWorkReportsViewSet(viewsets.ModelViewSet):
    serializer_class = DailyWorkReportsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.designation.id == 1:
            return DailyWorkReports.objects.filter(user=user)
        elif user.designation.id == 2:
            return DailyWorkReports.objects.filter(user__branch=user.branch, user__designation__id=1)
        else:
            return DailyWorkReports.objects.none()

    def perform_create(self, serializer):
        if self.request.user.designation.id == 1:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Only workers can add daily work reports.")



class ApplicationLeaveViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationLeaveSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self):
        user = self.request.user
        if user.designation.id == 1:  # Workers
            return ApplicationLeave.objects.filter(user=user)
        elif user.designation.id == 2:  # Managers

            return ApplicationLeave.objects.filter(user__branch=user.branch, user__designation__id=1)
        else:
            return ApplicationLeave.objects.none()

    def perform_create(self, serializer):
        if self.request.user.designation.id == 1:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Only workers can apply for leave.")

    def update(self, request, *args, **kwargs):
        leave_application = self.get_object()

        if request.user.designation.id == 2 and leave_application.user.branch == request.user.branch:
            if 'leave_status' in request.data:
                leave_application.leave_status = request.data['leave_status']
                leave_application.save(update_fields=['leave_status'])
                serializer = self.get_serializer(leave_application)
                return Response(serializer.data)
            else:
                return Response(
                    {"error": "Only the leave_status field can be updated."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            raise PermissionDenied("Only managers from the same branch can update the leave status.")
