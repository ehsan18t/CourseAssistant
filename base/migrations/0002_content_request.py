# Generated by Django 4.1.3 on 2022-12-15 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(default='', max_length=100)),
                ('course_code', models.CharField(default='', max_length=100)),
                ('semester', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
