# Generated by Django 2.1.7 on 2019-02-28 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secure_url', '0004_auto_20190227_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='securedentity',
            name='type',
            field=models.CharField(choices=[('links', 'Link'), ('files', 'File')], default='links', max_length=10),
        ),
    ]
