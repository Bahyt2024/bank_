from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ActivateView, UsersView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('activate/<str:link>/', ActivateView.as_view()),
    path('users/', UsersView.as_view()),
]
