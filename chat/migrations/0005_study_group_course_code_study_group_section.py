# Generated by Django 4.1.3 on 2022-12-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_group_message_is_read_read_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='study_group',
            name='course_code',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='study_group',
            name='section',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
