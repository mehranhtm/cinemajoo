from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
import requests
import json
from django.conf import settings
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserSerializer,
    MovieSerializer
)
from .models import UserProfile, Movie, UserMovieStatus

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_status(request):
    """Public endpoint to check API status"""
    return Response({
        'status': 'API is running',
        'message': 'Cinemajoo API is working correctly',
        'endpoints': {
            'register': '/api/register/',
            'login': '/api/login/',
            'profile': '/api/profile/',
            'user_info': '/api/user-info/',
            'check_username': '/api/check-username/',
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_test(request):
    """Simple public test endpoint"""
    return Response({
        'message': 'This is a public endpoint - no authentication required!',
        'status': 'success',
        'timestamp': '2024-01-01T00:00:00Z'
    }, status=status.HTTP_200_OK)

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User created successfully',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile)
            watched_total = UserMovieStatus.objects.filter(user=request.user, watched=True).count()
            data = serializer.data
            data['watched_total'] = watched_total
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_info(request):
    """Get current user information"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_username_availability(request):
    """Check if username is available"""
    username = request.data.get('username')
    if not username:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    is_available = not User.objects.filter(username=username).exists()
    return Response({
        'username': username,
        'is_available': is_available
    }, status=status.HTTP_200_OK)


class MovieSearchView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Avoid JWT auth errors on public endpoint

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        if not q:
            return Response({'error': 'Query parameter q is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # TMDB API configuration
        TMDB_API_KEY = 'f1849a9d40bee7e99593d0db724f6ddb'
        TMDB_BASE_URL = 'https://api.themoviedb.org/3'
        
        try:
            # Search movies from TMDB API
            search_url = f"{TMDB_BASE_URL}/search/movie"
            params = {
                'api_key': TMDB_API_KEY,
                'query': q,
                'language': 'en-US',
                'page': 1,
                'include_adult': False
            }
            
            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            movies = data.get('results', [])
            
            # Format the response to match our serializer
            formatted_movies = []
            for movie in movies[:20]:  # Limit to 20 results
                formatted_movie = {
                    'id': movie.get('id'),
                    'title': movie.get('title', ''),
                    'poster_url': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get('poster_path') else '',
                    'director': '',  # TMDB doesn't provide director in search results
                    'actors': '',   # TMDB doesn't provide actors in search results
                    'summary_en': movie.get('overview', ''),
                    'release_date': movie.get('release_date', ''),
                    'vote_average': movie.get('vote_average', 0),
                    'vote_count': movie.get('vote_count', 0)
                }
                formatted_movies.append(formatted_movie)
            
            return Response(formatted_movies, status=status.HTTP_200_OK)
            
        except requests.exceptions.RequestException as e:
            # Fallback to local database if TMDB API fails
            qs = Movie.objects.filter(title__icontains=q).order_by('title')[:20]
            return Response(MovieSerializer(qs, many=True).data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'Search failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, movie_id):
        """Get detailed movie information from TMDB API"""
        TMDB_API_KEY = 'f1849a9d40bee7e99593d0db724f6ddb'
        TMDB_BASE_URL = 'https://api.themoviedb.org/3'
        
        try:
            # Get movie details
            movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
            params = {
                'api_key': TMDB_API_KEY,
                'language': 'en-US',
                'append_to_response': 'credits'
            }
            
            response = requests.get(movie_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            credits = data.get('credits', {})
            
            # Extract director
            director = ''
            crew = credits.get('crew', [])
            for person in crew:
                if person.get('job') == 'Director':
                    director = person.get('name', '')
                    break
            
            # Extract main actors
            actors = []
            cast = credits.get('cast', [])
            for person in cast[:5]:  # Top 5 actors
                actors.append(person.get('name', ''))
            
            formatted_movie = {
                'id': data.get('id'),
                'title': data.get('title', ''),
                'poster_url': f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}" if data.get('poster_path') else '',
                'director': director,
                'actors': ', '.join(actors),
                'summary_en': data.get('overview', ''),
                'release_date': data.get('release_date', ''),
                'vote_average': data.get('vote_average', 0),
                'vote_count': data.get('vote_count', 0),
                'runtime': data.get('runtime', 0),
                'genres': [genre.get('name', '') for genre in data.get('genres', [])]
            }
            
            return Response(formatted_movie, status=status.HTTP_200_OK)
            
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Failed to fetch movie details'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({'error': 'Movie details request failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarkWatchedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'error': 'movie_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        status_obj, _ = UserMovieStatus.objects.get_or_create(user=request.user, movie=movie)
        if not status_obj.watched:
            status_obj.mark_watched()

        watched_total = UserMovieStatus.objects.filter(user=request.user, watched=True).count()
        return Response({
            'message': 'Movie marked as watched',
            'movie': MovieSerializer(movie).data,
            'watched_total': watched_total
        }, status=status.HTTP_200_OK)
