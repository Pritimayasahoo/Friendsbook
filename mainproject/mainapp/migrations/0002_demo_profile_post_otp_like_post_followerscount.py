# Generated by Django 4.2 on 2023-12-05 10:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='demo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='default.jpg', upload_to='profilepic')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_create', models.DateTimeField(default=datetime.datetime.now)),
                ('profileimage', models.ImageField(default='default.jpg', upload_to='profilepic')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('about', models.TextField(blank=True)),
                ('current_study', models.CharField(blank=True, max_length=50)),
                ('self_learner', models.BooleanField(default=False)),
                ('current_teach', models.CharField(blank=True, max_length=50)),
                ('backgroundimage', models.ImageField(default='default.jpg', upload_to='backgroundpic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('my_post', models.FileField(upload_to='allpost')),
                ('post_time', models.DateTimeField(default=datetime.datetime.now)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('no_of_like', models.IntegerField(default=0)),
                ('no_of_coment', models.IntegerField(default=0)),
                ('no_of_viewer', models.IntegerField(default=0)),
                ('caption', models.CharField(blank=True, max_length=150)),
                ('about', models.TextField(blank=True)),
                ('post_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('poster_profile', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.profile')),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=9)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like_post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('like_time', models.DateField(default=datetime.datetime.now)),
                ('like_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Followerscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followtime', models.DateTimeField(default=datetime.datetime.now)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]