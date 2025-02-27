from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/Goods/good_images/<filename>
    return f'Stationery_items/stationery_images/user_{instance.user.username}/{filename}'

class Stationery_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to=user_directory_path)  # Use custom path

    def __str__(self):
        return f'{self.name}'

    def delete(self, *args, **kwargs):
        # Check if the image file exists and delete it
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(Stationery_item, self).delete(*args, **kwargs)