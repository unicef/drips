from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import token_obtain_pair

urlpatterns = [
    path(r"drips/admin/", admin.site.urls),
    path(r"drips/api-token-auth/", token_obtain_pair),
    path(r"drips/api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(r"drips/security/", include("unicef_security.urls", namespace="security")),
    path(r"drips/social/", include("social_django.urls", namespace="social")),
    path(r"drips/api/", include("drips.api.urls", namespace="api")),
    path(r"drips/api/", include("sharepoint_rest_api.urls", namespace="sharepoint")),
    path(r"drips/accounts/", include("django.contrib.auth.urls")),
    path(r"drips/manage/adminactions/", include("adminactions.urls")),
    path(r"security/", include("unicef_security.urls")),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path(r"__debug__/", include(debug_toolbar.urls)),
    ]
