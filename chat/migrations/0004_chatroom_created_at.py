import django.utils.timezone as timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration to add the created_at field back to the ChatRoom model."""

    dependencies = [
        ('chat', '0003_alter_chatroom_options_remove_chatroom_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
    ]
