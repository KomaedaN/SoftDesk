from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from projects.models import Projects, Contributors, Issue, Comment
from projects.serializers import ProjectSerializer, CreateProjectSerializer, ProjectDetailSerializer, \
    UpdateProjectSerializer, DestroyProjectSerializer


class MultipleSerializerMixin:
    create_serializer_class = None
    retrieve_serializer_class = None
    update_serializer_class = None
    destroy_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.retrieve_serializer_class is not None:
            return self.retrieve_serializer_class
        elif self.action == 'create' and self.create_serializer_class is not None:
            return self.create_serializer_class
        elif self.action == 'update' and self.update_serializer_class is not None:
            return self.update_serializer_class
        elif self.action == 'destroy' and self.destroy_serializer_class is not None:
            return self.destroy_serializer_class

        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectSerializer
    create_serializer_class = CreateProjectSerializer
    retrieve_serializer_class = ProjectDetailSerializer
    update_serializer_class = UpdateProjectSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Projects.objects.filter(contributors__user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            if self.create_serializer_class is not None:
                project = Projects.objects.create(
                    title=request.data['title'],
                    description=request.data['description'],
                    type=request.data['type'],
                    author_user_id=request.user,
                )
                project.save()

                contributor = Contributors.objects.create(
                    user_id=request.user,
                    project_id=project,
                    permission='AUTHOR',
                )
                contributor.save()
                return Response(request.data)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            if self.update_serializer_class is not None:
                instance = self.get_object()
                update_project = Projects.objects.filter(id=instance.id).update(
                    title=request.data['title'],
                    description=request.data['description'],
                    type=request.data['type'],
                )
                return Response(request.data)

    def destroy(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            if request.user == self.get_object().author_user_id:
                instance = self.get_object()
                instance.delete()
                return Response('project delete')
            return Response('You are not the author')
