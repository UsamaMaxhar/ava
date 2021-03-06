from rest_framework import serializers

from ideas.models import Idea
from comments.serializers import CommentSerializer

class IdeaSerializer(serializers.ModelSerializer):
    ownername = serializers.ReadOnlyField(source='owner.username')
    
    comments = CommentSerializer(many=True)

    class Meta:
        model = Idea
        fields = (
                'id',
                'title',  
                'description', 
                'votes', 
                'ownername', 
                'owner',
                'created', 
                'edited', 
                'project',
                'comments')
