from django.db import models

class Article(models.Model):
    file_obj = models.ImageField(upload_to='media/')

class coordinate(models.Model):
    x = models.TextField()
    def __str__(self):
        return self.x

class Y_coordinate(models.Model):
    y = models.TextField()
    def __str__(self):
        return self.y