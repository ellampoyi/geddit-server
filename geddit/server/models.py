from django.db import models
from django.contrib.auth.models import User, AbstractUser

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


# class User(models.Model):
#     name = models.CharField(max_length=200)
#     mail = models.CharField(max_length=200, primary_key=True)
#     hash = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name

class CustomUser(AbstractUser):
    username = None
    mail = models.EmailField('mail', unique=True)

    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mail


class ListedErrand(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=260)
    from_location = models.CharField(max_length=200)
    to_location = models.CharField(max_length=200)
    errand_id = models.AutoField(primary_key=True)
    list_time = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

    def __str__(self):
        return (self.from_user.name + " " + self.list_time + " " + self.price + " " + self.description + " "
                + self.errand_id)


class AcceptedErrand(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=260)
    from_location = models.CharField(max_length=200)
    to_location = models.CharField(max_length=200)
    errand_id = models.IntegerField(primary_key=True)
    price = models.IntegerField()

    def __str__(self):
        return (self.from_user.name + " " + self.to_user.name + " " + self.price + " " + self.description + " "
                + self.errand_id)
