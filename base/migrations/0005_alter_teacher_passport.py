# Generated by Django 4.1.7 on 2024-05-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_teacher_cv_alter_teacher_flsc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='passport',
            field=models.ImageField(null=True, upload_to='teachers_passport'),
        ),
    ]
