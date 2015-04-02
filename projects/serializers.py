from rest_framework import serializers

from projects.models import Project
from rest_extensions.relations import HyperlinkedNestedRelatedField

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    ownername = serializers.ReadOnlyField(source='owner.username')
    owner_url = serializers.HyperlinkedRelatedField(
            view_name='user-detail', 
            source='owner', 
            read_only=True)
    
    ideas_count = serializers.ReadOnlyField(source='ideas.count')
    idea_list_url = HyperlinkedNestedRelatedField(
            view_name='idea-list',
            source='ideas',
            read_only=True,
            lookup_field='instance.pk',
            lookup_url_kwarg='project_pk'
            )
    class Meta:
        model = Project
        fields = (
                'title', 
                'url', 
                'description', 
                'status', 
                'ownername', 
                'owner_url',
                'ideas_count',
                'idea_list_url'
                  )

class ProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    ownername = serializers.ReadOnlyField(source='owner.username')
    owner_url = serializers.HyperlinkedRelatedField(
            view_name='user-detail', 
            source='owner', 
            read_only=True)

    idea_urls = HyperlinkedNestedRelatedField(
            view_name='idea-detail',
            read_only=True,
            many=True,
            source='ideas',
            lookup_url_kwarg='pk',
            additional_reverse_kwargs={"project_pk" : 'project_id'})

    class Meta:
        model = Project
        fields = ('title', 'url', 'description', 'ownername','owner_url', 'status', 'idea_urls')
