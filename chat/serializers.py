from rest_framework import serializers

from chat.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'title']

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Заголовок не может быть пустым")
        if len(value) > 200:
            raise serializers.ValidationError(
                "Заголовок не может быть длиннее 200 символов"
            )
        return value

class ChatDetailSerializer(serializers.ModelSerializer):
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
                limit = int(limit)
                if limit > 100:
                    limit = 100
                if limit < 1:
                    limit = 20
            except (TypeError, ValueError):
                limit = 20

        messages = Message.objects.filter(chat_id=obj.id).order_by('created_at')[:limit]

        return MessageSerializer(messages, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at']

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError("Текст сообщения не может быть пустым")
        if len(value) > 5000:
            raise serializers.ValidationError(
                "Текст сообщения не может быть длиннее 5000 символов"
            )
        return value