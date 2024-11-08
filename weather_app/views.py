from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
import logging
from .forms import studentsform, CityForm
from .models import City, profile
import json
from django.core.cache import cache
from django.utils import timezone

# Configure logging
logger = logging.getLogger(__name__)

# List of allowed IP addresses

allowed_ip = ['127.0.0.1']

def view_404(request, exception):
    return render(request, 'weather/404.html')

def get_client_ip(request):
    """Get client IP for rate limiting and IP restriction"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip

def check_ip_restriction(request):
    """Check if the client's IP is allowed"""
    client_ip = get_client_ip(request)
    if client_ip not in allowed_ip:
        logger.warning(f"Unauthorized access attempt from IP: {client_ip}")
        return False
    return True

def check_rate_limit(request, key_prefix):
    """
    Rate limiting function
    Limits to 5 attempts per 5 minutes per IP
    """
    if not check_ip_restriction(request):
        return False

    ip = get_client_ip(request)
    key = f"{key_prefix}:{ip}"
    attempts = cache.get(key, 0)
    
    if attempts >= 5:  # Max 5 attempts
        return False
    
    cache.set(key, attempts + 1, 300)  # 300 seconds = 5 minutes
    return True

def login_view(request):
    """Enhanced login view with security features"""

    if request.user.is_authenticated:
        return redirect('weather')

    if request.method == 'POST':
        if not check_rate_limit(request, "login"):
            if not check_ip_restriction(request):
                return HttpResponseForbidden("Your IP is restricted from accessing this site.")
            logger.warning(f"Rate limit exceeded for IP: {get_client_ip(request)}")
            return HttpResponseForbidden(
                "Too many login attempts. Please try again in 5 minutes."
            )

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both username and password are required')
            return render(request, 'weather/login.html')

        # Prevent timing attacks by using constant time comparison
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Set session expiry to 1 hour
                request.session.set_expiry(3600)
                
                # Clear failed login attempts
                cache.delete(f"login:{get_client_ip(request)}")
                
                # Log successful login
                logger.info(f"Successful login for user: {username}")
                
                # Set last login timestamp
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                
                next_url = request.GET.get('next', 'weather')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account is disabled')
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            messages.error(request, 'Invalid username or password')

    return render(request, 'weather/login.html')


@login_required
def logout_view(request):
    """Secure logout implementation"""
    logout(request)
    # Ensure session is cleared
    request.session.flush()
    return redirect('login')

# Decorator for requiring a fresh login for sensitive operations
def require_fresh_login(timeout_minutes=30):
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            last_login = request.user.last_login
            if not last_login or timezone.now() - last_login > timedelta(minutes=timeout_minutes):
                return redirect('login')
                
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator



@login_required
def new(request):
    try:
        user_profile = profile.objects.get()  
    except profile.DoesNotExist:
        user_profile = None
    cntext={
        'user_profile': user_profile
    }
    return render(request, 'weather/new.html',)

@login_required
def index(request):
    base_url = 'http://api.weatherapi.com/v1/current.json?key=2dc123b8b741441e966105202242002&q={}&aqi=no'
    err_msg = ''
    message = ''
    message_class = ''
    try:
        user_profile = profile.objects.get()  
    except profile.DoesNotExist:
        user_profile = None
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                url = base_url.format(new_city)
                r = requests.get(url).json()
                if 'error' not in r:  
                    form.save()
                else:
                    err_msg = 'City does not exist!'
            else:
                err_msg = 'City already exists!'
        
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added Successfully!'
            message_class = 'is_success'
    
    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        url = base_url.format(city.name)
        r = requests.get(url).json()
        if 'error' not in r:  
            city_weather = {
                'city': city.name,
                'temperature': r['current']['temp_c'],
                'description': r['current']['condition']['text'],
                'icon': r['current']['condition']['icon'],
            }
            weather_data.append(city_weather)
    
    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
        'user_profile': user_profile
    }
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')