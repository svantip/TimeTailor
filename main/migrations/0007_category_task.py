# Generated by Django 5.0.2 on 2024-02-18 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_task_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='task',
            field=models.ManyToManyField(to='main.task'),
        ),
    ]