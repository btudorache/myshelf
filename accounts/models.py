from django.urls import reverse
from django.db import models
from django.conf import settings
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, default='default.jpg', upload_to='users/')

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.user.username])

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.photo.path)
