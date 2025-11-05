from django.db import models
from django.conf import settings

class Prediction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="predictions")
	input_data = models.JSONField()
	result = models.JSONField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Prediction by {self.user.username} at {self.created_at}" 
