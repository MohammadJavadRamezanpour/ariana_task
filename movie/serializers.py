from rest_framework import serializers
from .models import Movie, Rating

class MovieSerializer(serializers.ModelSerializer):
    # this keeps the count of people who had rated for each movie
    voted_users_count = serializers.SerializerMethodField()

    # this keeps your vote, only if you voted, it wont exist if you didnt
    your_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'rating', 'voted_users_count', 'your_rating')

    def get_voted_users_count(self, movie):
        return movie.ratings.all().count()

    def get_your_rating(self, movie):
        try:
            # get user from serializers context if you can
            user = self.context['request'].user

            # get users reviews if you can
            return movie.ratings.get(user=user).score
        except:
            # if somthing wrong happend, return None, 
            # it will be deleted in 'to_representation' method
            return None

    def to_representation(self, movie):
        """
            we need to stop showing users vote on the movies he didnt vote for
            so with overriding this we delete 'your_rating' field from json output
        """

        # get the original representation
        representaiton = super().to_representation(movie)

        # rename request for simplicity
        request = self.context['request']

        # get user from serializers context, set it None if he is not authenticated
        user = request.user if request.user.is_authenticated else None

        # if user didnt vote, delete your_rating field
        if not movie.ratings.filter(user=user).exists():
            representaiton.pop('your_rating')
            
        return representaiton 


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['id', 'movie', 'score']

    def validate_score(self, value):
        """
            in this validation method we check if the score is between 0 and 10
        """
        if not 0 <= value <= 10:
            raise serializers.ValidationError("score should be between 0 and 10")
        return value
    
    def save(self, **kwargs):
        """
            we eigther create the rating record, or update it if already exists
        """

        # extract data we need from validated data and context
        score = self.validated_data['score']
        movie = self.validated_data['movie']
        user = self.context['request'].user

        # update the score or create it if doesnt exist
        # it returns the final object and a boolean representing
        # wether the object is created or opdated in a tuple
        # we unpacked it in obj and _
        obj, _ = Rating.objects.update_or_create(
            user=user, movie=movie,
            defaults={'score': score},
        )

        # return the object
        return obj