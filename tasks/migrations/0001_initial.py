# Generated by Django 5.1.4 on 2024-12-25 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('important', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('complete', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
