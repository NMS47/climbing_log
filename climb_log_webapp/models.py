from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator

# Create your models here.
class Users(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=30, unique=True, validators=[EmailValidator])
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(3) ,MaxValueValidator(100)])
    gender = models.CharField(max_length=7)
    user_pw = models.CharField(max_length=100)

class Climb_entry(models.Model):
    # user_id = models.ForeignKey(Users.user_id)
    user_id = models.PositiveIntegerField(primary_key=True, unique=True)
    date = models.DateField()
    place_name = models.CharField(max_length=40)
    place_coord = models.CharField(max_length=30)
    enviroment = models.CharField(max_length=20)
    climb_style = models.CharField(max_length=15)
    multipitches = models.BooleanField()
    num_pitches = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(15)] )
    grade = models.CharField(max_length=6)
    climber_position = models.CharField(max_length=15)
    ascent_type = models.CharField(max_length=20)
    num_attempts = models.PositiveSmallIntegerField()
    notes = models.TextField(max_length=400)
    entry_time = models.DateTimeField(auto_now=True)