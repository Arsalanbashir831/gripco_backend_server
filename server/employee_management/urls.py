# employee_management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserViewSet , BranchViewSet, DepartmentViewSet, DesignationViewSet, DailyWorkReportsViewSet, ApplicationLeaveViewSet , WorkerView, ManagerView

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'reports', DailyWorkReportsViewSet, basename='reports') 
router.register(r'leaves', ApplicationLeaveViewSet, basename='leaves')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
     path('users/worker/<int:branch_id>/', WorkerView.as_view(), name='worker-list'),
    path('users/manager/<int:branch_id>/', ManagerView.as_view(), name='manager-list'),
    path('', include(router.urls)),  # Include router URLs
]
