from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "api/",
        include("helloworld.urls")
    ),

    # DRF session login/logout
    path(
        "api-auth/",
        include("rest_framework.urls")
    ),

    path(
        "",
        RedirectView.as_view(
            url="/api/posts/",
            permanent=False
        )
    ),
]