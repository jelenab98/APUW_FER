from rest_framework import viewsets

from .serializers import AuthorSerializer, QuoteSerializer
from .models import Author, Quote


class AuthorAPI(viewsets.ModelViewSet):
    """
    retrieve:
        Return an author instance with their information (name and surname).

    list:
        Return all authors.

    create:
        Create a new author.

    delete:
        Remove an existing author.

    partial_update:
        Update one or more fields on an existing author.

    update:
        Update an author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class QuoteAPI(viewsets.ModelViewSet):
    """
    retrieve:
        Return a quote instance.

    list:
        Return all quotes.

    create:
        Create a new quote.

    delete:
        Remove an existing quote.

    partial_update:
        Update one or more fields on an existing quote.

    update:
        Update a quote.
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class AuthorQuoteAPI(viewsets.ModelViewSet):
    """
    retrieve:
        Return a quote instance for a specific author.

    list:
        Return all quotes for a specific author..

    create:
        Create a new quote for a specific author.

    delete:
        Remove an existing quote from a specific author.

    partial_update:
        Update one or more fields on an existing quote.

    update:
        Update a quote for a specific author.
    """
    serializer_class = QuoteSerializer

    def get_queryset(self):
        return Quote.objects.filter(author=self.kwargs['author_pk'])
