from django.db import models
from django.db import models
import datetime
# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Worker(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    # Age calculated from birthdate (derived field)
    age = models.IntegerField(null=True, blank=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    resume = models.FileField(upload_to='worker_resumes/')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE ,default=0)

    def save(self, *args, **kwargs):
        # Calculate age from birthdate
        if self.birth_date:
            today = datetime.date.today()
            self.age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name