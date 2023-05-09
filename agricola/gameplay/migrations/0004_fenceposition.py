# Generated by Django 4.1.5 on 2023-05-08 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0003_boardposition'),
    ]

    operations = [
        migrations.CreateModel(
            name='FencePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left', models.BooleanField(default=False)),
                ('top', models.BooleanField(default=False)),
                ('right', models.BooleanField(default=False)),
                ('bottom', models.BooleanField(default=False)),
                ('board_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameplay.boardposition')),
            ],
        ),
    ]
