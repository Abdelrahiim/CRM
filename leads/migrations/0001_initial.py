# Generated by Django 4.2.2 on 2023-07-09 13:35

import CRM.custom_config
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.CharField(default=CRM.custom_config.get_nano_id, max_length=12, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField(blank=True, null=True)),
                ('convert_to_client', models.BooleanField(default=False)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('high', 'High'), ('medium', 'Medium')], default='medium', max_length=10)),
                ('status', models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('won', 'Won'), ('low', 'Lost')], default='new', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads_team', to='team.team')),
            ],
        ),
        migrations.CreateModel(
            name='LeadFile',
            fields=[
                ('id', models.CharField(default=CRM.custom_config.get_nano_id, max_length=12, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='lead_files')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_files_user', to=settings.AUTH_USER_MODEL)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_files', to='leads.lead')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_files_team', to='team.team')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(default=CRM.custom_config.get_nano_id, max_length=12, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_lead', to='leads.lead')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_team', to='team.team')),
            ],
        ),
    ]
