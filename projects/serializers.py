from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from projects.models import Projects, Contributors, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author_user_id']

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
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id']
