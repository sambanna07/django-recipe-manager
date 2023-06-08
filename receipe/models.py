from django.db import models
from django.contrib.auth.models import User

class Receipe(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    receipe_name = models.CharField(max_length=100)
    receipe_description =models.TextField()
    receipe_image = models.ImageField(upload_to="receipe")


