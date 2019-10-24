from rest_framework import serializers

from wykop.accounts.serializers import UserSerializer
from wykop.posts.models import Post


# Serializers define the API representation.
class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        read_only_fields = ('author', )
        fields = ('url', 'id', 'title', 'text', 'author', 'created', 'score', 'image', 'video')

    author = UserSerializer(read_only=True)
