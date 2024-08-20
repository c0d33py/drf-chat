from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    """Model for storing user profile information."""

    class GenderChoices(models.TextChoices):
        """Choices for the gender field."""

        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='profile',
        verbose_name='User',
    )
    dob = models.DateField(
        null=True, blank=True, db_index=True, verbose_name='Birth Date'
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        blank=True,
        verbose_name='Gender Choice',
    )
    image = models.ImageField(
        upload_to='profile/',
        default='default/default-profile.jpg',
        help_text='If user is not set the profile image. The system automatically adds a default image for the user.',
        null=True,
        blank=True,
        verbose_name='Profile image',
    )

    class Meta:
        app_label = 'profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ['-id']

    def __str__(self):
        return str(self.user)
