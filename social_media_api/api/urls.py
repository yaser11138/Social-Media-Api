from django.urls import path, include

urlpatterns = [
    path('blog/', include('social_media_api.blog.urls')),
    path("auth/", include("social_media_api.authentication.urls")),
    path("users/", include("social_media_api.users.urls", ))

]
