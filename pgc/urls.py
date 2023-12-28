from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from vstup import views

from django.views.generic import RedirectView

urlpatterns = [
    path('', include('vstup.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
     path('vstup/', include('vstup.urls')),
]

# urlpatterns += [
#     path('', RedirectView.as_view(url='/vstup/', permanent=True)),
# ]


# для реєстраціїї  входу користувачів
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]


# static() - щоб додати відображення URL для статичних файлів (тільки на час розробки)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
