# Generated by Django 2.1.2 on 2018-12-24 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20181219_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_project', to='project.Project'),
        ),
    ]
