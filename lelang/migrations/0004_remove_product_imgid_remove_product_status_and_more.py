# Generated by Django 4.2.6 on 2023-11-02 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("lelang", "0003_image_rename_img_product_imgid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="imgid",
        ),
        migrations.RemoveField(
            model_name="product",
            name="status",
        ),
        migrations.AddField(
            model_name="product",
            name="img",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lelang.image",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="statusid",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="image",
            name="img",
            field=models.FileField(upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="status",
            name="status",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]