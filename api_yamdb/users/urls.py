from django.urls import path

from users import views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/token/', views.token, name='token'),
]
