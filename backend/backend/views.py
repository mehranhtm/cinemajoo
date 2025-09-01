from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home(request):
    """API Home/Index view"""
    return Response({
        "message": "Welcome to Cinemajoo API 🎬",
        "version": "1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "register": "/api/register/",
            "login": "/api/login/",
            "token_refresh": "/api/token/refresh/",
            "accounts": "/api/",   # هر چی تو accounts/urls تعریف کنی
        }
    }, status=status.HTTP_200_OK)
