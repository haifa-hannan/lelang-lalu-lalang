from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class Product(models.Model):
    productid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    prodname = models.CharField(blank=True, null=True, max_length=150)
    desc = models.TextField(blank=True, null=True)
    img = models.ForeignKey('Image', on_delete=models.CASCADE,blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    # status = models.ForeignKey('Status', on_delete=models.CASCADE, blank=True, null=True)
    statusid = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'

    # def soft_delete(self, deleted_by = None):
    #     self.chgby = deleted_by
    #     # self.endda = yesterday
    #     self.save()

    # def undelete(self, restored_by = None):
    #     self.endda = "2999-01-01"
    #     self.chgby = restored_by
    #     self.save()

    # def delete(self, using=None, keep_parents=False, deleted_by = None):
    #     self.soft_delete(deleted_by=deleted_by)
        
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

class Transaction(models.Model):
    transactionid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    productid = models.ForeignKey('product', on_delete=models.CASCADE, blank=True, null=True)
    lelangdate = models.DateTimeField(blank=True, null=True, default=timezone.now)
    lastprice = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    staffid = models.CharField(max_length=150, blank=True, null=True)
    userid = models.CharField(max_length=150, blank=True, null=True)
    statusid = models.CharField(max_length=150, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'transaction'
    

class Staffs(models.Model):    
    ROLE = [
        ("admin", "Admin"),
        ("staff", "Staff"),
    ]
    staffid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=5, choices=ROLE)
    uname = models.CharField(max_length=100, blank=True, null=True)
    pwd = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'staffs'

class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=150, blank=True, null=True)
    uname = models.CharField(max_length=100, blank=True, null=True)
    pwd = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'