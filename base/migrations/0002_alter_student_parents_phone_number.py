# Generated by Django 4.1.7 on 2024-05-07 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='parents_phone_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
