from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer


class ChatCreateView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer



class ChatDetailView(generics.RetrieveDestroyAPIView):
    queryset = Chat.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChatDetailSerializer
        else:
            return ChatSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, context={'request': request})

        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        chat_id = self.kwargs['pk']
        chat = get_object_or_404(Chat, id=chat_id)
        serializer.save(chat_id=chat)
