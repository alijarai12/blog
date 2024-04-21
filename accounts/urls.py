from .views import UserRegistrationView, UserLoginView
from django.urls import path
# from knox import views as knox_views

urlpatterns = [

    path('user/register/', UserRegistrationView.as_view(), name='register'),
    path('user/login/', UserLoginView.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    
]
