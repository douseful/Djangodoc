# Generated by Django 4.2 on 2023-04-21 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_articlepost_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecolumn',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
