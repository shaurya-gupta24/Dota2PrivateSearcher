# Generated by Django 4.0 on 2021-12-18 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privateApp', '0003_alter_match_end_time_alter_match_matchid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='matchId',
            field=models.BigIntegerField(unique=True),
        ),
    ]
