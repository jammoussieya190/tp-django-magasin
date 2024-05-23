from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from magasin import views


# urls.py
from django.urls import path
from magasin.views import generate_pdf

urlpatterns = [
    # Other URL patterns
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
 path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('magasin/', include('magasin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
  
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='register'),  # Utilisez la vue register de votre application magasin
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
