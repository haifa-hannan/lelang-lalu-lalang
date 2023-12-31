# Generated by Django 4.2.6 on 2023-11-02 02:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("lelang", "0002_rename_imgid_product_img"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "imgid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("img", models.FileField(blank=True, null=True, upload_to="")),
            ],
            options={
                "db_table": "image",
                "managed": True,
            },
        ),
        migrations.RenameField(
            model_name="product",
            old_name="img",
            new_name="imgid",
        ),
    ]
