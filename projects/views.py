from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from projects.permissions import ProjectPermission, ContributorPermission, IssuePermission
from authentication.models import User
from projects.models import Projects, Contributors, Issue, Comment
from projects.serializers import ProjectSerializer, CreateProjectSerializer, ProjectDetailSerializer, \
    UpdateProjectSerializer, ContributorSerializer, UserContributorSerializer, GetIssueSerializer, \
    CreateIssueSerializer, UpdateIssueSerializer


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

    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        return Projects.objects.filter(contributors__user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
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
            instance = self.get_object()
            update_project = Projects.objects.filter(id=instance.id).update(
                title=request.data['title'],
                description=request.data['description'],
                type=request.data['type'],
            )
            return Response(request.data)

    def destroy(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            instance = self.get_object()
            id = instance.id
            instance.delete()
            return Response(f'Project: {id} - {instance.title}, deleted')


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = UserContributorSerializer
    create_serializer_class = ContributorSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributors.objects.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):

        if request.method == 'POST':
            if self.create_serializer_class is not None:

                try:
                    project_users = Contributors.objects.get(user_id=request.POST['user_id'],
                                                             project_id=self.kwargs['project_pk'])
                    return Response('Error: this contributor is already in you project')
                except:
                    contributor = Contributors.objects.create(
                        user_id=User.objects.get(id=request.POST['user_id']),
                        project_id=Projects.objects.get(id=self.kwargs['project_pk']),
                        permission=request.data['permission'],
                    )
                    contributor.save()
                    return Response(request.data)

    def destroy(self, request, *args, **kwargs):
        current_project = Projects.objects.get(id=self.kwargs['project_pk'])
        if request.user == current_project.author_user_id:
            instance = self.get_object()
            instance.delete()
            return Response('contributor removed')
        else:
            return Response('You are not the project owner')


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = GetIssueSerializer
    create_serializer_class = CreateIssueSerializer
    update_serializer_class = UpdateIssueSerializer

    permission_classes = [IsAuthenticated, IssuePermission]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        project = self.kwargs['project_pk']
        author = request.user

        issue = Issue.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            tag=request.POST['tag'],
            priority=request.POST['priority'],
            status=request.POST['status'],
            project_id=Projects.objects.get(id=project),
            author_user_id=author,
            assignee_user_id=Contributors.objects.get(id=request.POST['assignee_user_id']),
        )
        issue.save()
        return Response(request.POST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        update_issue = Issue.objects.filter(id=instance.id).update(
            title=request.data['title'],
            description=request.data['description'],
            tag=request.data['tag'],
            priority=request.data['priority'],
            status=request.data['status'],
            assignee_user_id=Contributors.objects.get(id=request.POST['assignee_user_id']),
        )
        return Response(request.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response('issue removed')
