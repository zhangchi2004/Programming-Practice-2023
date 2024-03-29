# Generated by Django 4.2.4 on 2023-08-29 15:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_para_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="img_para",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="text_para",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
