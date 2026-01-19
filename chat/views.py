import logging
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

logger = logging.getLogger(__name__)

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer


class ChatCreateView(generics.CreateAPIView):
    """
    Представление для создания нового чата.

    Это представление позволяет создавать новый чат с использованием переданных данных.
    Используется стандартное поведение CreateAPIView из Django REST framework.
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer



class ChatDetailView(generics.RetrieveDestroyAPIView):
    """
    Представление для получения и удаления чата.

    Позволяет получить детальную информацию о чате с использованием сериализатора ChatDetailSerializer,
    а также удалить чат. При GET-запросе возвращается расширенная информация, при других методах —
    используется ChatSerializer. Удаление выполняется через переопределенный метод perform_destroy.
    """
    queryset = Chat.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChatDetailSerializer
        else:
            return ChatSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, context={'request': request})
        logger.info(f"Получен чат {obj.id}")
        return Response(serializer.data)

    def perform_destroy(self, instance):
        chat_id = instance.id
        instance.delete()
        logger.info(f"Чат {chat_id} успешно удален")
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageCreateView(generics.CreateAPIView):
    """
    Представление для создания нового сообщения в чате.

    Позволяет добавить сообщение в чат с указанным pk в URL. Перед сохранением
    получает объект чата через get_object_or_404 и привязывает сообщение к этому чату.
    """
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        chat_id = self.kwargs['pk']
        chat = get_object_or_404(Chat, id=chat_id)
        serializer.save(chat_id=chat)
        logger.info(f"Сообщение успешно создано в чате {chat_id}")
