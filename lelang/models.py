from django.db import models
import uuid

# Create your models here.
class Product(models.Model):
    productid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    prodname = models.CharField(blank=True, null=True, max_length=150)
    desc = models.TextField(blank=True, null=True)
    img = models.ForeignKey('Image', on_delete=models.CASCADE,blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    # status = models.ForeignKey('Status', on_delete=models.CASCADE, blank=True, null=True)
    statusid = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'
        
class Image(models.Model):
    imgid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    img = models.FileField(upload_to='images/')

    class Meta:
        managed = True
        db_table = 'image'

class Status(models.Model):
    statusid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(blank=True, null=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'status'        