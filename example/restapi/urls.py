from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from restapi import views

router = routers.DefaultRouter()
router.register('snippets1', views.SnippetList)

router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),

]
