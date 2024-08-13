from django.db import models
from django.contrib.auth import get_user_model


class Chat(models.Model):
    client = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='client_chats')
    support = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='support_chats',
                                blank=True, null=True)
    issue = models.CharField(max_length=150)
    # null на случай, когда ни один работник техподдержки
    # ещё не взялся за вопрос
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Chat of client {self.client.id} with'
                f'{self.support.id}')


class Message(models.Model):
    chat = models.ForeignKey(Chat,
                             on_delete=models.CASCADE,
                             related_name='messages')
    sender = models.ForeignKey(get_user_model(),
                               related_name='messages',
                               on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
