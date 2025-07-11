# from accounts.models import User
# from ratings.models import Product, Rating
# from django.core.files.base import ContentFile
# import random
# import os
# import django


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FakeRatingDetection.settings')  # Replace 'myproject' with your project name
# django.setup()
# # Create sample products
# products = [
#     {"name": "apple_iphone_15", "image_name": r"D:\saaswath\projects\SQL_injection\apple_iphone_15.jpg"},
#     {"name": "Bose SoundLink Speaker", "image_name": r"D:\saaswath\projects\SQL_injection\Bose SoundLink Speaker.jpg"},
#     {"name": "Canon EOS R6 Camera", "image_name": r"D:\saaswath\projects\SQL_injection\Canon EOS R6 Camera.jpg"},
#     {"name": "Dell XPS 13 Laptop.jpg", "image_name": r"D:\saaswath\projects\SQL_injection\Dell XPS 13 Laptop.jpg"},
#     {"name": "Fitbit Charge 6", "image_name": r"D:\saaswath\projects\SQL_injection\Fitbit Charge 6.jpg"},
#     {"name": "Kindle Paperwhite", "image_name": r"D:\saaswath\projects\SQL_injection\Kindle Paperwhite.jpg"},
#     {"name": "KitchenAid Stand Mixer", "image_name": r"D:\saaswath\projects\SQL_injection\KitchenAid Stand Mixer.jpg"},
#     # {"name": "Product 8", "image_name": "product8.jpg"},
#     # {"name": "Product 9", "image_name": "product9.jpg"},
#     # {"name": "Product 10", "image_name": "product10.jpg"},
# ]

# # Assuming you already have users created
# users = User.objects.all()

# # Add products and ratings
# for prod in products:
#     with open(f"path_to_images/{prod['image_name']}", "rb") as f:
#         image = ContentFile(f.read(), name=prod['image_name'])
#         product = Product.objects.create(name=prod["name"], image=image)
        
#         # Create ratings for each product
#         for user in users[:3]:  # Assume 3 users rate each product
#             Rating.objects.create(user=user, product=product, rating=round(random.uniform(1.0, 5.0), 2))

# import random
# from django.core.management.base import BaseCommand
# from accounts.models import User
# from ratings.models import Product, Rating
# from django.core.files.base import ContentFile

# import os
# import django


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FakeRatingDetection.settings')  # Replace 'myproject' with your project name
# django.setup()

# class Command(BaseCommand):
#     help = "Populate the database with sample products and ratings"

#     def handle(self, *args, **kwargs):
#         products = [
#            {"name": "apple_iphone_15", "image_name": r"D:\saaswath\projects\SQL_injection\apple_iphone_15.jpg"},
#     {"name": "Bose SoundLink Speaker", "image_name": r"D:\saaswath\projects\SQL_injection\Bose SoundLink Speaker.jpg"},
#     {"name": "Canon EOS R6 Camera", "image_name": r"D:\saaswath\projects\SQL_injection\Canon EOS R6 Camera.jpg"},
#     {"name": "Dell XPS 13 Laptop.jpg", "image_name": r"D:\saaswath\projects\SQL_injection\Dell XPS 13 Laptop.jpg"},
#     {"name": "Fitbit Charge 6", "image_name": r"D:\saaswath\projects\SQL_injection\Fitbit Charge 6.jpg"},
#     {"name": "Kindle Paperwhite", "image_name": r"D:\saaswath\projects\SQL_injection\Kindle Paperwhite.jpg"},
#     {"name": "KitchenAid Stand Mixer", "image_name": r"D:\saaswath\projects\SQL_injection\KitchenAid Stand Mixer.jpg"},
#         ]

#         users = User.objects.all()

#         for prod in products:
#             with open(f"D:\saaswath\projects\SQL_injection\{prod['image_name']}", "rb") as f:
#                 image = ContentFile(f.read(), name=prod['image_name'])
#                 product = Product.objects.create(name=prod["name"], image=image)

#                 # Create ratings for each product
#                 for user in users[:3]:  # Assume 3 users rate each product
#                     Rating.objects.create(
#                         user=user,
#                         product=product,
#                         rating=round(random.uniform(1.0, 5.0), 2)
#                     )
        
#         self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))

