# Generated by Django 3.2.12 on 2022-06-23 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voteapp', '0008_electionarea_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='votingstatus',
            name='electionarea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='voteapp.electionarea'),
        ),
    ]