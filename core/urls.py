from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static 
from drf_spectacular.views import ( 
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView,
)

drf_spectacular_urls = [ 
    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI (optional)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

apps_urls = [
    path('auth/',include('apps.users.urls'),name='auth-user'),
    path('auth/',include('apps.verification.urls'),name='auth-verify'),
]

urlpatterns = (
    [
        path('admin/', admin.site.urls),
    ] 
    + drf_spectacular_urls
    + apps_urls
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)