# Generated by Django 3.0.1 on 2020-02-24 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_activiti", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="activiticonfig",
            name="tenant",
            field=models.CharField(
                blank=True, default="tenant_1", max_length=100, verbose_name="tenant ID"
            ),
        ),
    ]
