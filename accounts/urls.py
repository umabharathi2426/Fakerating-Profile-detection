from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("",views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_user,name='logout'),
    path("user-list/",views.user_list,name="user-list"),
    path('block-user/<int:user_id>/',views.block_user,name="block-user")
]
