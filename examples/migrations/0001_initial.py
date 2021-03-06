# Generated by Django 2.1.11 on 2020-05-18 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Img_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('img_cnt', models.IntegerField(blank=True, null=True)),
                ('img_url_list', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parsed_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('notify', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('length', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('price', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('origin', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('style', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('model', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('mxratio', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('date', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('detail', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('color', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('size', models.CharField(blank=True, default='', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('url', models.URLField(default='')),
                ('shop_id', models.CharField(blank=True, default='', max_length=50)),
                ('shop_password', models.CharField(blank=True, default='', max_length=50)),
                ('path', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='parsed_data',
            name='f_k',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='examples.Shop'),
        ),
        migrations.AddField(
            model_name='img_data',
            name='f_k',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='img_data', to='examples.Parsed_data'),
        ),
    ]
