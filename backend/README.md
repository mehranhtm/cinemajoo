# Cinemajoo Django Backend

This is the Django backend for the Cinemajoo project, providing user authentication and management APIs.

## Features

- User registration and login with JWT authentication
- User profile management
- Secure password validation
- CORS support for frontend integration
- RESTful API endpoints

## Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser --username admin --email admin@example.com --password your_password

# Or use custom command
python manage.py createsuperuser --username admin --email admin@example.com --password your_password
```

### 3. Run the Server

```bash
# Start Django development server
python manage.py runserver

# The server will run on http://localhost:8000
```

## API Endpoints

### Authentication Endpoints

- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `GET /api/accounts/profile/` - Get user profile
- `PUT /api/accounts/profile/` - Update user profile
- `GET /api/accounts/user-info/` - Get current user info
- `POST /api/accounts/check-username/` - Check username availability

### JWT Token Endpoints

- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

## API Usage Examples

### User Registration

```javascript
const response = await fetch('http://localhost:8000/api/accounts/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'testuser',
    email: 'test@example.com',
    password: 'SecurePass123!',
    confirm_password: 'SecurePass123!',
    first_name: 'Test',
    last_name: 'User'
  })
});
```

### User Login

```javascript
const response = await fetch('http://localhost:8000/api/accounts/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'testuser',
    password: 'SecurePass123!'
  })
});
```

### Authenticated Request

```javascript
const response = await fetch('http://localhost:8000/api/accounts/profile/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  }
});
```

## Models

### UserProfile

- `user` - OneToOneField to Django User model
- `phone_number` - Optional phone number
- `date_of_birth` - Optional date of birth
- `profile_picture` - Optional profile picture
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp

## Security Features

- JWT token-based authentication
- Password validation with complexity requirements
- CORS configuration for frontend security
- CSRF protection
- Secure password hashing

## Development

### Adding New Endpoints

1. Create views in `accounts/views.py`
2. Add serializers in `accounts/serializers.py` if needed
3. Update URL patterns in `accounts/urls.py`
4. Test with the Django development server

### Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test accounts
```

## Configuration

The main configuration is in `backend/settings.py`:

- Database settings (SQLite by default)
- JWT token configuration
- CORS settings
- REST framework settings
- Installed apps and middleware

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure the frontend URL is in `CORS_ALLOWED_ORIGINS`
2. **Database errors**: Run `python manage.py migrate` to apply migrations
3. **Import errors**: Check that all dependencies are installed
4. **Port conflicts**: Change the port in `runserver` command if needed

### Logs

Check the Django console output for detailed error messages and debugging information.

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Use a production database (PostgreSQL, MySQL)
3. Configure proper CORS settings
4. Set up HTTPS
5. Use environment variables for sensitive settings
6. Configure static file serving
7. Set up proper logging

## Support

For issues and questions, check the Django documentation or create an issue in the project repository.







