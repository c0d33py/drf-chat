from django.db import migrations


class Migration(migrations.Migration):
    """Migration for removing the name field from the ChatRoom model."""

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='name',
        ),
    ]
