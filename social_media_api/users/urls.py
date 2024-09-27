from django.urls import path
from .apis import ProfileApi, RegisterApi
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterApi.as_view(),name="register"),
    path('profile/', ProfileApi.as_view(),name="profile"),
]
