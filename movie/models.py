from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()

    @property
    def rating(self) -> float:
        """
            this calculates the average rating of a ovie
            Returns(float): the average
        """

        # we get this from the annotation in the view
        if hasattr(self, '_rating') and self._rating is not None:
            return self._rating
        return 0

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        # we dont want a user to have two ratings on one movie
        unique_together = ['user', 'movie']
