
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	ROLE_CHOICES = [
		("admin", "Admin"),
		("clinician", "Clinician"),
		("patient", "Patient"),
	]
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")
	full_name = models.CharField(max_length=150, default="John Doe")
	medical_license = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f"{self.email} ({self.role})"
