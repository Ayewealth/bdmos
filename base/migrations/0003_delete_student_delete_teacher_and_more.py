# Generated by Django 4.1.7 on 2024-04-23 16:08

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city_or_town',
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='user',
            name='disability',
        ),
        migrations.RemoveField(
            model_name='user',
            name='religion',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state_of_origin',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('STUDENT', 'Student'), ('TEACHER', 'Teacher')], default='ADMIN', max_length=50),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('student_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('religion', models.CharField(choices=[('christian', 'CHRISTIAN'), ('muslim', 'MUSLIM'), ('others', 'OTHERS')], max_length=30)),
                ('disability', models.CharField(choices=[('yes', 'YES'), ('no', 'NO')], max_length=20)),
                ('state_of_origin', models.CharField(blank=True, max_length=100, null=True)),
                ('city_or_town', models.TextField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('base.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('religion', models.CharField(choices=[('christian', 'CHRISTIAN'), ('muslim', 'MUSLIM'), ('others', 'OTHERS')], max_length=30)),
                ('disability', models.CharField(choices=[('yes', 'YES'), ('no', 'NO')], max_length=20)),
                ('state_of_origin', models.CharField(blank=True, max_length=100, null=True)),
                ('city_or_town', models.TextField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('base.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
