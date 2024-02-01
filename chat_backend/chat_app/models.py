from django.db import models


class ChatMessage(models.Model):
    """
    Model representing a chat message.

    Attributes:
    - text (TextField): The content of the message.
    - sender (CharField): The sender of the message, limited to 50 characters.
    - session_id (CharField): The session ID associated with the message, limited to 255 characters, defaulting to an empty string.
    """
    text = models.TextField()
    sender = models.CharField(max_length=50)
    session_id = models.CharField(max_length=255, default='')
