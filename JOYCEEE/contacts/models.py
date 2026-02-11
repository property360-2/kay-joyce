# contacts/models.py
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)  # MAKE SURE THIS LINE EXISTS
    category = models.CharField(max_length=50, blank=True)

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "notes": self.notes,
            "category": self.category,
        }

    def __str__(self):
        return self.name