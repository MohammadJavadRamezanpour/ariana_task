from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieView.as_view(), name="movie_view"),
    path('rate/', RatingView.as_view(), name="rating_view"),
]