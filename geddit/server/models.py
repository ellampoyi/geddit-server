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


class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ListedErrand(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=260)
    errand_id = models.AutoField(primary_key=True)
    list_time = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

    def __str__(self):
        return self.from_user.name + " " + self.status


class AcceptedErrand(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=260)
    errand_id = models.IntegerField(primary_key=True)
    price = models.IntegerField()

    def __str__(self):
        return self.from_user.name + " " + self.status
