from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from restapi import views
from .doc_urls import urlpatterns as doc_urlpatterns

router = routers.DefaultRouter()
router.register('snippets1', views.SnippetList)

router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]

# restframework
urlpatterns += [
    path('', include(router.urls)),
]
# docurls
urlpatterns += doc_urlpatterns

urlpatterns += [
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('auth/token/', obtain_auth_token,name="token"),
]
