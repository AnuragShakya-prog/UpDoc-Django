from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.


class Document(models.Model):
    document_name=models.CharField(max_length=100)
    document_image=models.ImageField(upload_to="users/documents/")
    document_owner=models.ForeignKey(User,on_delete=models.CASCADE)
    outline_image=models.ImageField(upload_to="users/temp/outlineimages/",null=True)

    def delete(self,*args, **kwargs):
        image=self.document_image
        outline_image=self.outline_image
        # Removing file
        os.remove(image.path)
        os.remove(outline_image.path)
        super().delete(*args,**kwargs)

