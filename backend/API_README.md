# Cinemajoo API Documentation

## 🚀 Server Status
✅ **Server is running successfully!**

## 📍 Available Endpoints

### Main Page
- **GET** `/` - Welcome page with API information

### API Status
- **GET** `/api/status/` - Public API status check (no authentication required)

### Authentication
- **POST** `/api/register/` - User registration (no authentication required)
- **POST** `/api/login/` - User login (no authentication required)
- **POST** `/api/logout/` - User logout (requires authentication)
- **GET** `/api/user-info/` - Get current user information (requires authentication)
- **POST** `/api/check-username/` - Check username availability (no authentication required)

### JWT Tokens
- **POST** `/api/token/` - Get JWT access token
- **POST** `/api/token/refresh/` - Refresh JWT token

### User Profile
- **GET** `/api/profile/` - Get user profile
- **PUT** `/api/profile/` - Update user profile

### Admin
- **GET** `/admin/` - Django admin panel

## 🔧 How to Test

### 1. Test Home Page (Public)
```bash
curl http://localhost:8000/
```

### 2. Test API Status (Public)
```bash
curl http://localhost:8000/api/status/
```

### 3. Test Registration (Public)
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

### 4. Test Login (Public)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### 5. Test Protected Endpoint (Requires Token)
```bash
# First get a token from login, then use it:
curl -X GET http://localhost:8000/api/user-info/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Run Complete Test Suite
```bash
python test_api.py
```

## 🎉 Success!
All previous errors have been resolved:
- ✅ `pkg_resources` error fixed
- ✅ `ImportError: register` error fixed
- ✅ URL patterns properly configured
- ✅ Server running without errors
