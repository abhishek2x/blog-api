from django.contrib import admin
from django.urls import path, include, re_path

# drf_yasg code starts here
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blogging App API",
        default_version='v1',
        description="Welcome to the world of Blogging",
        terms_of_service="https://abhisheksrivastava.tech",
        contact=openapi.Contact(email="abhisheksrivastavabbn@gmail.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ends here

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  #<-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  #<-- Here

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]


# /spec.json (json spec of API doc)
# /spec.yaml (yaml spec of API doc)
# /doc (Our nice pretty Swagger UI view of API doc)
# /redoc (A pretty Redoc view of API doc)
