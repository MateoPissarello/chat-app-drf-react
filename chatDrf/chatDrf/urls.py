from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from server.views import ServerListViewSet

router = routers.DefaultRouter()
router.register(r"api/server/select", ServerListViewSet, basename="server")
urlpatterns = [
    path("admin/", admin.site.urls),
    # Optional UI:
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/schema/ui/", SpectacularSwaggerView.as_view(), name="swagger_ui"),
] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
