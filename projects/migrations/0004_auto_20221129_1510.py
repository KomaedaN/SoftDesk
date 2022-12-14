# Generated by Django 3.2.16 on 2022-11-29 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_alter_projects_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='description',
            field=models.CharField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='projects',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(choices=[('BACKEND', 'Back-end'), ('FRONTEND', 'Front-end'), ('IOS', 'IOS'), ('ANDROID', 'Android')], max_length=15),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1500)),
                ('tag', models.CharField(choices=[('BUG', 'Bug'), ('IMPROVEMENT', 'Improvement'), ('TASK', 'Task')], max_length=12)),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'HIGH')], default='LOW', max_length=6)),
                ('status', models.CharField(choices=[('TO DO', 'To do'), ('IN PROGRESS', 'In progress'), ('DONE', 'Done')], default='TO DO', max_length=12)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assignee_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.contributors')),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projects')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1500)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('issue_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.issue')),
            ],
        ),
    ]
