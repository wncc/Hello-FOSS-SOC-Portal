from django.db import models
from django.contrib.auth.models import User
from .options import DepartmentChoices, YearChoices
from django.core.exceptions import ValidationError

def upload_to_location(instance, filename):
    return "profile_pictures/{filename}".format(filename=filename)


def validate_roll_number(value):
    # Extract the first two digits (batch/year) to determine the format
    batch_number = int(value[:2])

    if batch_number >= 22:
        # For batches >= 22, the format is BBPXXXX (no specific constraint on P)
        if not value[2:3].isalpha() or not value[3:].isdigit() or len(value) != 7:
            raise ValidationError("Enter a valid roll number.")
    else:
        # For batches < 22, the format is YYPDDCNNN (no specific constraint on P, DD, or C)
        if not (len(value) == 9 and value[2].isalpha() and value[3:5].isalpha() and value[5:6].isdigit() and value[6:].isdigit()):
            raise ValidationError("Enter a valid roll number.")



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=100, blank=True, default="")
    profile_picture = models.ImageField(
        upload_to=upload_to_location, blank=True, default=""
    )
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    roll_number = models.CharField(
        "roll number",
        max_length=9,
        unique=True,
        help_text="Required. 9 characters or fewer.", # Adjust max_length to 9 to accommodate the longest format (YYPDDCNNN)
        validators=[validate_roll_number],
        error_messages={
            "unique": "A user with that roll number already exists.",
        },
    )
    year = models.CharField(choices=YearChoices.choices, null=False, blank=False, max_length=100)
    department = models.CharField(
        max_length=50, choices=DepartmentChoices.choices, blank=False, null=False
    )

    verified = models.BooleanField(default=False)

    verification_token = models.CharField(max_length=32, blank=True, default="")



    
    # Add more fields as required

    def __str__(self):
        return f"{self.roll_number} - {self.user.username}"
