from django.urls import path
from chat import views

urlpatterns = [
    path('chats/', views.ChatCreateView.as_view(), name='chat-create'),
    path('chats/<int:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
    path('chats/<int:pk>/messages/', views.MessageCreateView.as_view(), name='message-create'),
    ]