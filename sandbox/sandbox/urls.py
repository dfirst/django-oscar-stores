from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.i18n import javascript_catalog
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

js_info_dict = {
    'packages': ('stores',),
}

urlpatterns = [
    url(r'^dashboard/stores/', apps.get_app_config('stores_dashboard').urls),
    url(r'^stores/', apps.get_app_config('stores').urls),
    url(r'^', include(apps.get_app_config('oscar').urls[0])),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict,
        name="javascript-catalogue"),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
