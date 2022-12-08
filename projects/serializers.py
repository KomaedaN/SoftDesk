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


class UserContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user_id', 'permission']


class GetIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CreateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority', 'status', 'assignee_user_id']


class UpdateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority', 'status', 'assignee_user_id']


class GetCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author_user_id', 'description']


class CreateCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description']


class UpdateCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description']


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
