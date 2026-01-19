from django.db import models

from chat.validators import validate_title, validate_text


class Chat(models.Model):
    """Модель чата.

    Представляет чат с уникальным названием и датой создания.
    Название автоматически проверяется на корректность при сохранении.

    Attributes:
        title (str): Название чата, не может быть пустым.
        created_at (datetime): Дата и время создания чата, устанавливается автоматически.

    Methods:
        clean(): Очищает и валидирует поле title.
        save(*args, **kwargs): Выполняет полную валидацию перед сохранением.
        __str__(): Возвращает строковое представление чата.
    """

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ["-created_at"]

    title = models.CharField(null=False, blank=False, max_length=200, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def clean(self):
        self.title = validate_title(str(self.title))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Чат #{self.id}: {self.title}"


class Message(models.Model):
    """Модель сообщения.

    Представляет сообщение в чате, привязанное к конкретному чату.
    Содержит текст сообщения и дату его создания. Текст автоматически
    проверяется на корректность при сохранении.

    Attributes:
        chat_id (Chat): Ссылка на чат, к которому относится сообщение.
                       При удалении чата сообщение также удаляется.
        text (str): Текст сообщения, не может быть пустым, максимум 5000 символов.
        created_at (datetime): Дата и время создания сообщения, устанавливается автоматически.

    Methods:
        clean(): Очищает и валидирует поле text.
        save(*args, **kwargs): Выполняет полную валидацию перед сохранением.
        __str__(): Возвращает строковое представление сообщения с обрезанным текстом.
    """

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(null=False, blank=False, max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        self.text = validate_text(str(self.text))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        prev = self.text[:50] if len(self.text) > 50 else self.text
        return f"Сообщение #{self.id} от {self.created_at}: {prev}"
