from django.conf import settings
from django.urls import path
from rest_framework import routers
from django.conf.urls import include, url

from .views import UserViewSet, DomainViewSet, PasswordViewSet, EmailViewSet, BulkUploadViewSet
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('domain', DomainViewSet)
router.register('password', PasswordViewSet)
router.register('email', EmailViewSet)
router.register('bulk_upload', BulkUploadViewSet, basename="upload")
urlpatterns = [
    path('', include(router.urls)),
]
