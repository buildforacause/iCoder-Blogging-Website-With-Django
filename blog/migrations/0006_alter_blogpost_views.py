# Generated by Django 4.0.5 on 2022-06-06 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogpost_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]