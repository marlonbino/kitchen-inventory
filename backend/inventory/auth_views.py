from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import UserProfile
import json


@csrf_exempt
def register(request):
    """
    Public registration endpoint is disabled for security.
    User creation is now restricted to administrators only.
    Use the Django admin panel or admin-only user management API.
    """
    return JsonResponse({
        'error': 'Public registration is disabled. Contact your administrator for access.',
        'message': 'For security reasons, only administrators can create new user accounts.'
    }, status=403)


@csrf_exempt
def login_view(request):
    """
    Login a user.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return JsonResponse(
            {'error': 'Username and password are required.'},
            status=400
        )
    
    # Authenticate user
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Create or get token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Get or create user profile
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'kitchen_staff'}
        )
        
        # Log the user in
        login(request, user)
        
        return JsonResponse({
            'message': 'Login successful.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': profile.role
            },
            'token': token.key
        }, status=200)
    else:
        return JsonResponse(
            {'error': 'Invalid username or password.'},
            status=401
        )


@csrf_exempt
def logout_view(request):
    """
    Logout the current user.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    
    logout(request)
    return JsonResponse(
        {'message': 'Logout successful.'},
        status=200
    )


@api_view(['GET'])
def user_info(request):
    """
    Get current user information including role.
    """
    if request.user.is_authenticated:
        # Get or create user profile
        profile, profile_created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'role': 'kitchen_staff'}
        )
        
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'role': profile.role
        }, status=200)
    else:
        return JsonResponse(
            {'error': 'Not authenticated.'},
            status=401
        )


@api_view(['POST'])
def admin_create_user(request):
    """
    Admin-only endpoint to create new users.
    Only users with 'admin' role can create new users.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    
    # Check if user is admin
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'admin':
            return JsonResponse({
                'error': 'Permission denied. Only administrators can create users.'
            }, status=403)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found.'}, status=403)
    
    # Get data from request
    data = request.data
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')
    role = data.get('role', 'kitchen_staff')
    
    if not username or not password:
        return JsonResponse({
            'error': 'Username and password are required.'
        }, status=400)
    
    # Validate role
    valid_roles = ['kitchen_staff', 'manager', 'admin']
    if role not in valid_roles:
        return JsonResponse({
            'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'
        }, status=400)
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            'error': 'Username already exists.'
        }, status=400)
    
    # Password validation
    if len(password) < 8:
        return JsonResponse({
            'error': 'Password must be at least 8 characters long.'
        }, status=400)
    
    # Create new user
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Create user profile with specified role
        profile = UserProfile.objects.create(
            user=user,
            role=role
        )
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return JsonResponse({
            'message': 'User created successfully.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': profile.role
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to create user: {str(e)}'
        }, status=400)


@api_view(['GET'])
def admin_list_users(request):
    """
    Admin-only endpoint to list all users.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    
    # Check if user is admin
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'admin':
            return JsonResponse({
                'error': 'Permission denied. Only administrators can view users.'
            }, status=403)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found.'}, status=403)
    
    # Get all users with their profiles
    users = User.objects.all().order_by('-date_joined')
    user_list = []
    
    for user in users:
        try:
            profile = UserProfile.objects.get(user=user)
            role = profile.role
        except UserProfile.DoesNotExist:
            role = 'kitchen_staff'
        
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role,
            'date_joined': user.date_joined.isoformat(),
            'is_active': user.is_active
        })
    
    return JsonResponse({'users': user_list}, status=200)


@api_view(['DELETE'])
def admin_delete_user(request, user_id):
    """
    Admin-only endpoint to delete a user.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=401)
    
    # Check if user is admin
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'admin':
            return JsonResponse({
                'error': 'Permission denied. Only administrators can delete users.'
            }, status=403)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found.'}, status=403)
    
    # Prevent admin from deleting themselves
    if request.user.id == user_id:
        return JsonResponse({
            'error': 'You cannot delete your own account.'
        }, status=400)
    
    # Delete the user
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        return JsonResponse({
            'message': f'User "{username}" deleted successfully.'
        }, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to delete user: {str(e)}'
        }, status=400)
