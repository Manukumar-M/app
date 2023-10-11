from django.urls import include, path, reverse_lazy
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from openwisp_firmware_upgrader.private_storage.urls import (
    urlpatterns as fw_private_storage_urls,
)
redirect_view = RedirectView.as_view(url=reverse_lazy('admin:index'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('openwisp_controller.urls')),
    path('api/v1/', include('openwisp_utils.api.urls')),
    path('api/v1/', include('openwisp_users.api.urls')),
    path('', include('openwisp_firmware_upgrader.urls')),
    path(
        '',
        include((fw_private_storage_urls, 'firmware'), namespace='firmware'),
    ),

    path('', include('openwisp_monitoring.urls')),
    path('', redirect_view, name='index'),

]

urlpatterns += staticfiles_urlpatterns()
