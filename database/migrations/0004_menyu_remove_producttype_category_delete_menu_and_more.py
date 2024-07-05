# Generated by Django 5.0.6 on 2024-07-05 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_remove_menu_description_remove_menu_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menyu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
            ],
            options={
                'db_table': 'menu',
            },
        ),
        migrations.RemoveField(
            model_name='producttype',
            name='category',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='ProductType',
        ),
    ]
