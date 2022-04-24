from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Avg


# Create your views here.
class MovieView(ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        """
          we use prefetch_related for optimization
          we have a huge number of reviews for each movie
          prefetch_related does a separate lookup for each relationship, and performs the joining in python
          we annotate the _rating to the queryset and send it from model to the serializer
          i think this is much more faster and optimized
        """
        return Movie.objects.prefetch_related('ratings').all().annotate(_rating=Avg('ratings__score'))
    
    def get_serializer_context(self):
        return {'request': self.request}


class RatingView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated] # only authenticated users can vote

    def get_serializer_context(self):
        return {'request': self.request}