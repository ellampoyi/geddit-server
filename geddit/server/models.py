from django.db import models

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=200)
#     phone = models.CharField(max_length=10)
# 
#     def __str__(self):
#         return self.name
# 
# class Errand(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     status = models.CharField(max_length=100)
# 
#     def __str__(self):
#         return self.user.name + " " + self.status
