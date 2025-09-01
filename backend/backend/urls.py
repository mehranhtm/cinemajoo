from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # Local app endpoints
    path('api/', include('accounts.urls')),

    # JWT auth endpoints
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
