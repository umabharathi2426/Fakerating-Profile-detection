from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name ="ratings"

urlpatterns = [
    path('rate/<int:product_id>/', views.rate_product, name='rate_product'),
    path("products/", views.list_all_product, name="product_list")
]
