# Generated by Django 2.1.11 on 2020-06-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0013_auto_20200602_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsed_data',
            name='category',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='parsed_data',
            name='storeName',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]