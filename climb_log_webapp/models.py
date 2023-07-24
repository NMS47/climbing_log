from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator, MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class ClimbEntry(models.Model):
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_of_climb = models.DateField()
    place_name = models.ForeignKey("ClimbPlaces", on_delete=models.CASCADE)
    climb_style = models.CharField(max_length=15)
    multipitches = models.BooleanField()
    num_pitches = models.PositiveSmallIntegerField(default=1, null=True, blank=True, validators=[MaxValueValidator(15)] )
    grade = models.CharField(max_length=20)
    grade_equivalent =  models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(15)] )
    climber_position = models.CharField(max_length=15, default='lead', null=True, blank=True,)
    ascent_type = models.CharField(max_length=20, default='flash', null=True, blank=True,)
    num_attempts = models.PositiveSmallIntegerField(default=1, null=True, blank=True,)
    notes = models.TextField(max_length=400, default='No hay notas',null=True, blank=True)
    date_of_entry = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}, {self.grade}, {self.date_of_climb}"
    
    class Meta:
        ordering = ["date_of_climb"]

class ClimbPlaces(models.Model):
    place_name = models.CharField(max_length=50, unique=True)
    place_coords = models.CharField(max_length=50, unique=True)
    enviroment = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.place_name}"

# For a coming upgrade for easier climbing place addition
# class ClimbPlacesCSV(CsvDbModel):

#     class Meta:
#         delimiter = ";"
#         dbModel = ClimbPlaces
#         has_header = True

class UserInfo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sex = models.CharField(max_length=15, null=True, blank=True, default='unknown')
    age =  models.PositiveSmallIntegerField(default=1, null=True, blank=True, validators=[MaxValueValidator(110)] )
    nationality = models.CharField(max_length=15, null=True, blank=True, default='Citizen of the World')
    profile_pic = models.ImageField(null=True, blank=True, default='profile-icon.png')