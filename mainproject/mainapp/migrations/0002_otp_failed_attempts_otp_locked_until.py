# Generated by Django 4.2 on 2024-01-01 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='failed_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='otp',
            name='locked_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]