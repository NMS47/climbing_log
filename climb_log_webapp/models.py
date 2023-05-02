from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator, MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class Climb_entry(models.Model):
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_of_climb = models.DateField()
    place_name = models.CharField(max_length=40)
    place_coord = models.CharField(max_length=30, null=True, blank=True)
    enviroment = models.CharField(max_length=20)
    climb_style = models.CharField(max_length=15)
    multipitches = models.BooleanField()
    num_pitches = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(15)] )
    grade = models.CharField(max_length=20)
    climber_position = models.CharField(max_length=15)
    ascent_type = models.CharField(max_length=20)
    num_attempts = models.PositiveSmallIntegerField()
    notes = models.TextField(max_length=400)
    date_of_entry = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}, {self.grade}, {self.date_of_climb}"
    
    class Meta:
        ordering = ["date_of_climb"]