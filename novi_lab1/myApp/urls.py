from rest_framework_nested.routers import NestedSimpleRouter, DefaultRouter
from django.conf.urls import url, include

from .views import AuthorAPI, QuoteAPI, AuthorQuoteAPI

router = DefaultRouter()
router.register(r'quotes', QuoteAPI)
router.register(r'authors', AuthorAPI)

authors_router = NestedSimpleRouter(router, r'authors', lookup='author')
authors_router.register(r'quotes', AuthorQuoteAPI, basename='author-quotes')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(authors_router.urls)),
]
