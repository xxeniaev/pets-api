# Generated by Django 3.2.4 on 2021-06-07 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210607_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='created_at',
            field=models.DateField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pet',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]