# Generated by Django 4.0.2 on 2022-02-20 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('LnF', '0001_initial'),
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lnf_post',
            name='booth',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.booth'),
        ),
    ]
