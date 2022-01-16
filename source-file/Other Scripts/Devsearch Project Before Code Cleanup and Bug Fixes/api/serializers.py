from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer): # serializer for review
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # to work with nested objects
    owner = ProfileSerializer(many=False)  # this connected to a profile. many=False: we don't have multiple profiles or multiple owners. We're going to have just one.
    tags = TagSerializer(many=True)  # this connected to a tag. many=True: we do want multiple tags. (many to many)
    reviews = serializers.SerializerMethodField()  # reviews are a child object with different query. to add in a attribute into this JSON object by using a method field.

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):  # self: does not refer to the model. It's going to refer to this serializer class. obj: is going to be the object that we're serializing, which will be this project (model = Project).
        reviews = obj.review_set.all()  # So this just gets all of our projects reviews
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data  # to return the serializer data

