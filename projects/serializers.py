from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework_nested import relations

from projects.models import Project
from users.serializers import UserSerializer
from ideas.serializers import IdeaSerializer
from ideas.models import Idea

class HyperlinkedNestedRelatedField(serializers.HyperlinkedRelatedField):
    def __init__(self, view_name=None, additional_reverse_kwargs={}, **kwargs):
        self.additional_reverse_kwargs = additional_reverse_kwargs
        super(HyperlinkedNestedRelatedField, self).__init__(view_name, **kwargs)

    def to_representation(self, value):
        request = self.context.get('request', None)
        format = self.context.get('format', None)

        return self.get_url(value, self.view_name, request, format)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, returh the URL that hyperlinks to the object

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field` 
        attributes are not configured to correctly match the URL conf.
        """
        print("made it here")
        kwargs = {}
        print(self.additional_reverse_kwargs)
        if 'list' in self.view_name:
            kwargs[self.lookup_url_kwarg: self.source.pk]
        for key, value in self.additional_reverse_kwargs.items():
            kwargs[key] = getattr(obj, value, None)
        print(self.lookup_url_kwarg)
        if 'detail' in self.view_name:
            kwargs.update({self.lookup_url_kwarg: getattr(obj, self.lookup_field)})
        print(kwargs)
        print("view name: {}".format(view_name))
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    ownername = serializers.ReadOnlyField(source='owner.username')
    owner_url = serializers.HyperlinkedRelatedField(
            view_name='user-detail', 
            source='owner', 
            read_only=True)
    
    ideas_count = serializers.ReadOnlyField(source='ideas.count')
    idea_list = HyperlinkedNestedRelatedField(
            view_name='idea-list',
            source='ideas',
            lookup_field='all',
            read_only=True,
            additional_reverse_kwargs={"project_pk" : "pk"})

    class Meta:
        model = Project
        fields = ('title', 
                  'url', 
                  'description', 
                  'status', 
                  'ownername', 
                  'owner_url',
                  'ideas_count',
                  'idea_list')

class ProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    ownername = serializers.ReadOnlyField(source='owner.username')
    owner_url = serializers.HyperlinkedRelatedField(
            view_name='user-detail', 
            source='owner', 
            read_only=True)

    idea_url = HyperlinkedNestedRelatedField(
            view_name='idea-detail',
            read_only=True,
            source='idea',
            additional_reverse_kwargs={"project_pk" : "pk"})

    class Meta:
        model = Project
        fields = ('title', 'url', 'description', 'ownername','owner_url', 'status', 'idea_url')
