from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('city/', views.index, name='home'),
    path('weather/', views.new, name='weather'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('login/', views.login_view, name='login'),
    path('out/', views.logout_view, name='out'),
    path('', lambda request: redirect('login')),  # Redirects to login if the base URL is accessed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.view_404
