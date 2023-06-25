from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_width = 972
    max_height = 422 
    img = Image.open(image)
    if img.width > max_width or img.height > max_height:
        raise ValidationError("Максимальные допустимые размеры изображения - 972x422 пикселей.")

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='media/event/', validators=[validate_image_size])
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'События'

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/category/', validators=[validate_image_size])
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
    
class Exhibit(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/exhibit_images/')
    description = models.TextField()
    audio = models.FileField(upload_to='media/exhibit_audio/', null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name = ("Категория"), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        return self.title
