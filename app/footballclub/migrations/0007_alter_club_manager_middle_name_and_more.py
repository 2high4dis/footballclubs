# Generated by Django 4.2 on 2023-07-14 15:56

from django.db import migrations, models
import footballclub.models


class Migration(migrations.Migration):

    dependencies = [
        ('footballclub', '0006_alter_city_city_alter_club_base_alter_club_city_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='manager_middle_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[footballclub.models.validate_string], verbose_name='Manager`s middle name'),
        ),
        migrations.AlterField(
            model_name='enemyteam',
            name='coach_middle_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[footballclub.models.validate_string], verbose_name='Coach middle name'),
        ),
    ]