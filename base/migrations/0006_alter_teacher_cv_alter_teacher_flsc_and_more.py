# Generated by Django 4.1.7 on 2024-05-16 11:13

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_teacher_passport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='cv',
            field=models.FileField(null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to="cv's"),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='flsc',
            field=models.FileField(null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='teacher_documents'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='other_certificate',
            field=models.FileField(null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='other_certificate'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='secondary_school_transcript',
            field=models.FileField(null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='teacher_documents'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='university_polytech_institution_cer',
            field=models.FileField(null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='teacher_documents'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='university_polytech_institution_cer_trans',
            field=models.FileField(null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='teacher_documents'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='waec_neco_nabteb_gce',
            field=models.FileField(null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='teacher_documents'),
        ),
    ]