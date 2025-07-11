from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Rating
from django.contrib.auth.decorators import login_required

@login_required
def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    existing_rating = Rating.objects.filter(user=request.user, product=product).first()
    
    if request.method == 'POST':
        rating = float(request.POST['rating'])
        time_taken = request.POST.get('rating_time', '')  # Get the time taken from the form
        
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.time_taken = time_taken
            existing_rating.save()
        else:
            Rating.objects.create(
                user=request.user, 
                product=product, 
                rating=rating,
                time_taken=time_taken
            )
        return redirect('ratings:product_list')
    
    context = {
        'product': product,
        'existing_rating': existing_rating
    }
    return render(request, 'create_rating.html', context)

@login_required
def list_all_product(request):
    # Check if user is fake based on their ratings
    user = request.user
    if not user.is_staff:  # Don't check staff users
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
        
        # If user is detected as fake, block them and log them out
        if suspicious_count > 3:
            from django.contrib.auth import logout
            from django.contrib import messages
            user.is_blocked = True
            user.save()
            messages.error(request, "Your account has been blocked please contact admin")
            logout(request)
            return redirect('accounts:home')

    # Continue with normal product list view if user is not fake
    products = Product.objects.all()
    product_ratings = []
    
    for product in products:
        ratings = Rating.objects.filter(product=product).values_list('rating', flat=True)
        user_rating = Rating.objects.filter(user=request.user, product=product).first()
        has_rated = user_rating is not None
        
        product_ratings.append({
            'product': product,
            'ratings': list(ratings),
            'has_rated': has_rated,
            'time_taken': user_rating.time_taken if user_rating else None
        })
    
    context = {
        'product_ratings': product_ratings,
    }
    return render(request, 'product_list.html', context)
