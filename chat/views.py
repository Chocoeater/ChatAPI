import logging

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer
from chat.validators import validate_limit

logger = logging.getLogger(__name__)


class ChatCreateView(generics.CreateAPIView):
    """
    Представление для создания нового чата.
    """

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatDetailView(generics.RetrieveDestroyAPIView):
    """
    Представление для получения и удаления чата.
    """

    queryset = Chat.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.method != "GET":
            return qs

        limit = self._get_limit()

        messages_qs = Message.objects.order_by("-created_at")[:limit]

        return qs.prefetch_related(
            Prefetch(
                'messages',
                queryset=messages_qs,
                to_attr='last_messages'
            )
        )

    def _get_limit(self) -> int:
        raw_limit = self.request.query_params.get('limit')
        try:
            return validate_limit(int(raw_limit))
        except (ValueError, TypeError, ValidationError):
            return 20


    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatDetailSerializer
        else:
            return ChatSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, context={"request": request})
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
    """

    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, id=chat_id)
        serializer.save(chat_id=chat)
        logger.info(f"Сообщение успешно создано в чате {chat_id}")
