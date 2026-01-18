from django.core.exceptions import ValidationError
from django.db import models


class Chat(models.Model):
    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ['created_at']

    title = models.CharField(null=False, blank=False, max_length=200, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def clean(self):
        self.title = self.title.strip()
        if not self.title:
            raise ValidationError({
                'title': 'Название не может быть пустым'
            })
        if len(self.title) > 200:
            raise ValidationError({
                'title': 'Название не может быть длиннее 200 символов'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Чат #{self.id}: {self.title}"


class Message(models.Model):
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['created_at']

    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False, max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.text:
            raise ValidationError({
                'text': 'Текст сообщения не может быть пустым'
                })
        if len(self.text) > 5000:
            raise ValidationError({
                'text': 'Текст сообщения не может быть длиннее 5000 символов'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        prev = self.text[:50] if len(self.text) > 50 else self.text
        return f"Сообщение #{self.id} от {self.created_at}: {prev}"