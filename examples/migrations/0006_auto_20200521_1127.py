# Generated by Django 2.1.11 on 2020-05-21 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0005_parsed_data_size2'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsed_data',
            name='dateasd',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='parsed_data',
            name='date',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]