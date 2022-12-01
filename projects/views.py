from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from projects.models import Projects, Contributors, Issue, Comment
from projects.serializers import ProjectSerializer, CreateProjectSerializer, ProjectDetailSerializer


class MultipleSerializerMixin:
    create_serializer_class = None
    retrieve_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.retrieve_serializer_class is not None:
            return self.retrieve_serializer_class
        elif self.action == 'create' and self.create_serializer_class is not None:
            return self.create_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectSerializer
    create_serializer_class = CreateProjectSerializer
    retrieve_serializer_class = ProjectDetailSerializer

    def get_queryset(self):

        return Projects.objects.filter(author_user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        test = Projects.objects.filter(id=12)
        if self.create_serializer_class is not None:
            contributor = Contributors.objects.create(
                user_id=request.user.id,
                project_id=self.pk,
                permission='AUTHOR',
            )
            contributor.save()
            return contributor
