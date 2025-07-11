from django.urls import path
from . import views

app_name ='detection'

urlpatterns = [
    path('upload/', views.upload_files, name='upload_files'),
    path('train/', views.train_model, name='train_model'),
    path('predict/', views.predict, name='predict'),
]
