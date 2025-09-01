from django.urls import path
from .views import (
    api_status,
    public_test,
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserLogoutView,
    get_user_info,
    check_username_availability
)

urlpatterns = [
    path('status/', api_status, name='api-status'),
    path('test/', public_test, name='public-test'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-info/', get_user_info, name='user-info'),
    path('check-username/', check_username_availability, name='check-username'),
]


