# Generated by Django 4.2.1 on 2023-06-06 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0004_playercard'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerboardstatus',
            name='pen_num',
            field=models.IntegerField(default=0),
        ),
    ]