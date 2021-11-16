from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import*

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', download_view, name='download')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)