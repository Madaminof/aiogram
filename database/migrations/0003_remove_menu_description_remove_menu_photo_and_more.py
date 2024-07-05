# Generated by Django 5.0.6 on 2024-07-05 05:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_alter_menu_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='description',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='price',
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.menu')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
