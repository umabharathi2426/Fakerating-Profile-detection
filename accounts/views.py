# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('ratings:product_list')  # Direct redirect to products page
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is blocked before logging in
            if user.is_blocked:
                messages.error(request, "Your account has been blocked please contact admin")
                return redirect('accounts:home')
            
            login(request, user)
            if user.is_staff:
                return redirect('admin:index')  # Admin goes to admin page
            else:
                return redirect('ratings:product_list')  # Normal users go to products page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('accounts:home')

# Add middleware to check if user is blocked
@login_required
def check_if_blocked(request):
    if request.user.is_authenticated and request.user.is_blocked:
        messages.error(request, "Your account has been blocked please contact admin")
        logout(request)
        return redirect('accounts:home')
    return None

@login_required
def user_list(request):
    if not request.user.is_staff:
        return redirect('accounts:home')
    
    from ratings.models import Rating, Product

    users = User.objects.all()
    for user in users:
        if not user.is_staff:  # Don't block staff/admin users
            # Count suspicious ratings
            suspicious_count = 0
            for product in Product.objects.all():
                rating = Rating.objects.filter(user=user, product=product).first()
                if rating and rating.time_taken:
                    try:
                        # Parse time string like "0m 12s" or "12s"
                        time_str = rating.time_taken.lower()
                        total_seconds = 0
                        
                        # Handle minutes
                        if 'm' in time_str:
                            minutes_part = time_str.split('m')[0].strip()
                            if minutes_part:
                                total_seconds += int(minutes_part) * 60
                            time_str = time_str.split('m')[1]
                        
                        # Handle seconds
                        if 's' in time_str:
                            seconds_part = time_str.split('s')[0].strip()
                            if seconds_part:
                                total_seconds += int(seconds_part)
                        
                        if total_seconds < 10 and (float(rating.rating) == 1.0 or float(rating.rating) == 5.0):
                            suspicious_count += 1
                    except:
                        pass
            
            # Automatically block user if they have more than 3 suspicious ratings
            if suspicious_count > 3 and not user.is_blocked:
                user.is_blocked = True
                user.save()
    
    return render(request, 'user_list.html', {'users': users})

@login_required
def block_user(request, user_id):
    if not request.user.is_staff:
        return redirect('accounts:home')
    
    user = User.objects.get(id=user_id)
    if not user.is_staff:  # Prevent blocking admin users
        user.is_blocked = not user.is_blocked
        user.save()
    return redirect('accounts:user-list')