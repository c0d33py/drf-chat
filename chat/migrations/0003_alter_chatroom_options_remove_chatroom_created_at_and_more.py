from django.db import migrations


class Migration(migrations.Migration):
    """Migration for altering ChatRoom options, removing created_at field, and deleting TypingIndicator model."""

    dependencies = [
        ('chat', '0002_remove_chatroom_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatroom',
            options={
                'verbose_name': 'chat room',
                'verbose_name_plural': 'chat rooms',
            },
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='created_at',
        ),
        migrations.DeleteModel(
            name='TypingIndicator',
        ),
    ]
