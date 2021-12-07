from .models import User, Quote
from .serializers import UserSerializer, QuoteSerializer
from rest_framework import viewsets


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QuoteAPI(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


# TODO: dodati novi view s filtracijom po foreign key