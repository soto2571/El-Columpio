from django.db import models

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    num_of_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.customer_name} on {self.date} at {self.time}"
