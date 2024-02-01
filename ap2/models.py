from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models


class CustomUser(models.Model):
    ROLES = (
        ('patient', 'Patient'),
        ('staff', 'Staff'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,default=None)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.user.username

class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)  # Assuming a standard international phone number format
    services = models.TextField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name


from django.contrib.auth.models import User  # Assuming you are using the built-in User model

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date_of_review = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.clinic.name} - {self.rating}"



class Queueing(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    appointment_id = models.AutoField(primary_key=True)
    appointment_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.clinic.name} - {self.status}"

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Queueing, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.clinic.name} - {self.payment_date}"
