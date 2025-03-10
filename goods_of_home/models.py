from django.db import models
from django.contrib.auth.models import User
import os

# Custom function to define the upload path
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/Goods/good_images/<filename>
    return f'Goods/good_images/user_{instance.user.username}/{filename}'

class Good(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    good_name = models.CharField(max_length=250)
    good_description = models.TextField()
    good_location = models.TextField(null=True, blank=True)
    good_collection = models.TextField(null=True, blank=True)
    good_image = models.ImageField(upload_to=user_directory_path)  # Use custom path

    def __str__(self):
        return f'{self.good_name}'

    def delete(self, *args, **kwargs):
        # Check if the image file exists and delete it
        if self.good_image:
            if os.path.isfile(self.good_image.path):
                os.remove(self.good_image.path)
        super(Good, self).delete(*args, **kwargs)