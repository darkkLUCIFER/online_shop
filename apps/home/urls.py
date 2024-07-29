from django.urls import path

from apps.home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('bucket/', views.BucketHomeView.as_view(), name='bucket'),
]
