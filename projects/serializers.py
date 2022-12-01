import requests
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from projects.models import Projects, Contributors, Issue, Comment
from authentication.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['user_id', 'permission']


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'type']

    """def create(self, data):
        project = Projects.objects.create(
            title=data['title'],
            description=data['description'],
            type=data['type'],
            author_user_id=self.request.user.id,
        )
        project.save()
        return project"""


class ProjectDetailSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']

    def get_contributors(self, instance):
        queryset = instance.contributors.filter(project_id=instance.id)
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data


class UpdateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type']
