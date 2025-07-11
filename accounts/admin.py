from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from ratings.models import Rating, Product
from django.contrib.auth.models import Group
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    def get_list_display(self, request):
        products = Product.objects.all()
        # Dynamically create methods for each product
        for product in products:
            method_name = f'time_for_{product.name.lower().replace(" ", "_")}'
            if not hasattr(self, method_name):
                setattr(self, method_name, self._create_product_method(product))
                # Set column header to product name
                getattr(self, method_name).short_description = product.name
        
        return ('colored_username',) + tuple(f'time_for_{p.name.lower().replace(" ", "_")}' for p in products)

    def _create_product_method(self, product):
        def get_rating_time(obj):
            rating = Rating.objects.filter(user=obj, product=product).first()
            if rating:
                time_str = f"{rating.time_taken}" if rating.time_taken else ""
                rating_str = f"(Rating: {int(rating.rating)})" if rating.rating else ""
                if time_str or rating_str:
                    return f"{time_str} {rating_str}".strip()
            return ""
        return get_rating_time

    def is_suspicious_rating(self, rating):
        if not rating or not rating.time_taken:
            return False
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
            
            return total_seconds < 10 and (float(rating.rating) == 1.0 or float(rating.rating) == 5.0)
        except:
            return False

    def colored_username(self, obj):
        # Count suspicious ratings
        suspicious_count = 0
        for product in Product.objects.all():
            rating = Rating.objects.filter(user=obj, product=product).first()
            if self.is_suspicious_rating(rating):
                suspicious_count += 1
        
        if suspicious_count > 3:
            # Automatically block the user if they are detected as fake
            if not obj.is_staff and not obj.is_blocked:  # Don't block staff users
                obj.is_blocked = True
                obj.save()
            return format_html(
                '<span style="color: red;">{} (Fake User)</span>',
                obj.username
            )
        return obj.username
    colored_username.short_description = 'Username'

    search_fields = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    list_filter = []  # Remove all filters

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# Register your models here.
admin.site.register(User, CustomUserAdmin)
# Remove Groups from admin interface
admin.site.unregister(Group)