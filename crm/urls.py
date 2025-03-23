from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls', namespace='lead')),

    path("__reload__/", include("django_browser_reload.urls")),
]
