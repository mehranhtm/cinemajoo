# Cinemajoo API Endpoints Guide

## 🔓 Public Endpoints (No Authentication Required)

### ✅ These endpoints work without any token:

1. **Home Page**
   - URL: `GET /`
   - Description: Welcome page with API information

2. **API Status**
   - URL: `GET /api/status/`
   - Description: Check if API is running

3. **Public Test**
   - URL: `GET /api/test/`
   - Description: Simple test endpoint

4. **User Registration**
   - URL: `POST /api/register/`
   - Description: Create new user account

5. **User Login**
   - URL: `POST /api/login/`
   - Description: Login and get JWT tokens

6. **Check Username**
   - URL: `POST /api/check-username/`
   - Description: Check if username is available

## 🔒 Protected Endpoints (Authentication Required)

### ❌ These endpoints require a valid JWT token:

1. **User Info**
   - URL: `GET /api/user-info/`
   - Requires: `Authorization: Bearer <token>`

2. **User Profile**
   - URL: `GET /api/profile/`
   - Requires: `Authorization: Bearer <token>`

3. **Update Profile**
   - URL: `PUT /api/profile/`
   - Requires: `Authorization: Bearer <token>`

4. **User Logout**
   - URL: `POST /api/logout/`
   - Requires: `Authorization: Bearer <token>`

## 🧪 How to Test

### Test Public Endpoints:
```bash
# Test home page
curl http://localhost:8000/

# Test API status
curl http://localhost:8000/api/status/

# Test public endpoint
curl http://localhost:8000/api/test/
```

### Test Protected Endpoints:
```bash
# First, get a token by logging in
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Then use the token
curl -X GET http://localhost:8000/api/user-info/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🚨 Common Issues

### HTTP 401 Unauthorized Error
If you get this error, it means:
- You're trying to access a protected endpoint without a token
- Your token has expired
- Your token is invalid

### Solution:
1. Use only public endpoints for initial testing
2. Get a valid token by logging in first
3. Include the token in your request headers

## 🎯 Quick Test Commands

```bash
# Run the simple test script
python simple_test.py

# Or test manually
curl http://localhost:8000/api/test/
```









