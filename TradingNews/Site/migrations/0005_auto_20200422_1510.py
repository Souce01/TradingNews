# Generated by Django 3.0.5 on 2020-04-22 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0004_auto_20200422_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='network',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Network',
        ),
    ]
