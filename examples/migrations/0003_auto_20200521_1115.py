# Generated by Django 2.1.11 on 2020-05-21 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0002_auto_20200521_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parsed_data',
            name='date',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
