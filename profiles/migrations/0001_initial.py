import django.db.models.deletion as django
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    '''Migration for creating the Profile model.'''

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'dob',
                    models.DateField(
                        blank=True, db_index=True, null=True, verbose_name='Birth Date'
                    ),
                ),
                (
                    'gender',
                    models.CharField(
                        max_length=1,
                        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
                        blank=True,
                        verbose_name='Gender Choice',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        upload_to='profile/',
                        default='default/default-profile.jpg',
                        help_text='If user is not set the profile image. The system automatically adds a default image for the user.',
                        blank=True,
                        null=True,
                        verbose_name='Profile image',
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.CASCADE,
                        related_name='profile',
                        verbose_name='User',
                        null=True,
                    ),
                ),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'ordering': ['-id'],
            },
        ),
    ]
