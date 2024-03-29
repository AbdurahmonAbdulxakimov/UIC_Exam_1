# Generated by Django 4.2.7 on 2024-02-23 14:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_lessonviewed_last_viewed"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="lesson",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="lessonviewed",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="lessonviewed",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
