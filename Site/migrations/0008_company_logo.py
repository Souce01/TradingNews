# Generated by Django 3.0.6 on 2020-05-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0007_company_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.CharField(max_length=200, null=True),
        ),
    ]