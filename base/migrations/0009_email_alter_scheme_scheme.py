# Generated by Django 5.0.6 on 2024-05-22 22:26

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_teacher_cv_alter_teacher_flsc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.EmailField(blank=True, max_length=254, null=True)),
                ('subject', models.CharField(blank=True, max_length=500, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='scheme',
            name='scheme',
            field=models.FileField(storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='scheme'),
        ),
    ]
