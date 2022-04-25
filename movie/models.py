from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .task import cely_mail

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
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        # we dont want a user to have two ratings on one movie
        unique_together = ['user', 'movie']


@receiver(post_save, sender=Movie)
def send_email(sender, instance, **kwargs):
    """
    this signal runs after each movie being created
    this actually sends email to every user in the database
    but the email is not real, it just shows the email in terminal
    """
    cely_mail.delay(f"{instance.title} movie just piblished", "this movie is so fun\ndont miss it ;)", "info@email.com", [user.email for user in get_user_model().objects.all()])
