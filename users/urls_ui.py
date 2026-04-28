from django.urls import path
from .ui_views import login_view, register_view, logout_view

urlpatterns = [
    path('login/', login_view, name='ui_login'),
    path('register/', register_view, name='ui_register'),
    path('logout/', logout_view, name='ui_logout'),
]
