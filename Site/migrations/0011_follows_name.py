# Generated by Django 3.0.6 on 2020-10-20 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0010_auto_20200926_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='follows',
            name='name',
            field=models.CharField(default='null', max_length=50),
        ),
    ]
