from django.db import models
import uuid

# Create your models here.
class Product(models.Model):
    productid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    prodname = models.CharField(blank=True, null=True, max_length=150)
    desc = models.TextField(blank=True, null=True)
    imgid = models.ImageField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    status = models.CharField(blank=True, null=True, max_length=150)

    class Meta:
        managed = True
        db_table = 'product'

class Status(models.Model):
    statusid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(blank=True, null=True, max_length=150)

    class Meta:
        managed = True
        db_table = 'status'

        
class Image(models.Model):
    imgid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    img = models.FileField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'image'