# Generated by Django 4.1.3 on 2022-11-13 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_lesson_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
