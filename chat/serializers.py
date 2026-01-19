from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from chat.models import Chat, Message
from chat.validators import validate_limit, validate_title, validate_text


class ChatSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Chat.
    
    Преобразует объекты модели Chat в формат JSON и обратно.
    Валидирует поле 'title' с использованием кастомного валидатора.
    
    Поля:
        id (int): Уникальный идентификатор чата.
        title (str): Название чата.
    """

    class Meta:
        model = Chat
        fields = ['id', 'title']

    def validate_title(self, value: str) -> str:
        return validate_title(value)


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Message.
    
    Преобразует объекты модели Message в формат JSON и обратно.
    Валидирует поле 'text' с использованием кастомного валидатора.
    
    Поля:
        id (int): Уникальный идентификатор сообщения.
        text (str): Текст сообщения.
        created_at (datetime): Дата и время создания сообщения.
    """

    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at']

    def validate_text(self, value: str) -> str:
        return validate_text(value)


class ChatDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор детальной информации о чате.
    
    Используется для отображения информации о чате вместе с последними сообщениями.
    Поддерживает параметр limit через query-параметры запроса для ограничения количества возвращаемых сообщений.
    
    Поля:
        id (int): Уникальный идентификатор чата.
        title (str): Название чата.
        messages (list): Список последних сообщений в чате (ограничено значением limit).
    
    Методы:
        get_messages(obj) -> list: Возвращает сериализованные последние сообщения из чата с учётом лимита.
    """

    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'title', 'messages']

    def get_messages(self, obj):
        request = self.context.get('request')
        limit = 20

        if request and request.query_params.get('limit'):
            try:
                limit = int(request.query_params.get('limit'))
                limit = validate_limit(limit)
            except (ValidationError, TypeError, ValueError):
                limit = 20

        messages = Message.objects.filter(chat_id=obj.id).order_by('-created_at')[:limit]

        return MessageSerializer(messages, many=True).data