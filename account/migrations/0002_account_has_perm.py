# Generated by Django 3.0.3 on 2022-03-28 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='has_perm',
            field=models.BooleanField(default=True),
        ),
    ]
