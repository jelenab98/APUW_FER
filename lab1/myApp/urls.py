from django.conf.urls import url, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from .views import UserAPI, QuoteAPI

router = DefaultRouter()
router.register(r'quotes', QuoteAPI)
router.register(r'users', UserAPI)

users_router = NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'quotes', QuoteAPI, basename='user-quotes')  # TODO: dodati drugi view s filtracijom


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
]
