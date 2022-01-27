from django.contrib import admin
from django.urls import include, path

# Importa as variaveis do settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('item.urls')),
]
