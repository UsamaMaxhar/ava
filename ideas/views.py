from ideas.models import Idea
from ideas.serializers import IdeaSerializer, IdeaDetailSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class IdeaViewSet(viewsets.ModelViewSet):
    """
    This viewset automagically provides 'list', 'create', 'retrieve', 'update', and 'destroy' actions
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, pk=None):
        queryset = Idea.objects.all()
        idea = get_object_or_404(queryset, pk=pk)
        if pk is None:
            serializer = IdeaSerializer(idea)
        else:
            serializer = IdeaDetailSerializer(idea, 
                                              context={'request':request})

        return Response(serializer.data)
