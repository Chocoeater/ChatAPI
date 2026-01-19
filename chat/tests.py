from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import Chat, Message
from chat.validators import validate_title, validate_text, validate_limit

class ChatModelTest(TestCase):
    
    def setUp(self):
        self.chat = Chat.objects.create(title="Тестовый чат")
        
    def test_chat_creation(self):
        """Тест создания чата"""
        self.assertEqual(self.chat.title, "Тестовый чат")
        self.assertIsNotNone(self.chat.created_at)
        
    def test_chat_string_representation(self):
        """Тест строкового представления чата"""
        self.assertEqual(str(self.chat), f"Чат #{self.chat.id}: Тестовый чат")
        
    def test_chat_ordering(self):
        """Тест сортировки чатов"""
        chat2 = Chat.objects.create(title="Другой тестовый чат")
        chats = list(Chat.objects.all())
        self.assertEqual(chats[0], chat2)  # Самый новый первый
        

class MessageModelTest(TestCase):
    
    def setUp(self):
        self.chat = Chat.objects.create(title="Тестовый чат")
        self.message = Message.objects.create(
            chat_id=self.chat,
            text="Тестовое сообщение"
        )
        
    def test_message_creation(self):
        """Тест создания сообщения"""
        self.assertEqual(self.message.text, "Тестовое сообщение")
        self.assertEqual(self.message.chat_id, self.chat)
        self.assertIsNotNone(self.message.created_at)
        
    def test_message_string_representation(self):
        """Тест строкового представления сообщения"""
        expected_text = self.message.text[:50] if len(self.message.text) > 50 else self.message.text
        expected = f"Сообщение #{self.message.id} от {self.message.created_at}: {expected_text}"
        self.assertEqual(str(self.message), expected)
        
    def test_message_ordering(self):
        """Тест сортировки сообщений"""
        message2 = Message.objects.create(
            chat_id=self.chat,
            text="Другое тестовое сообщение"
        )
        messages = list(Message.objects.all())
        self.assertEqual(messages[0], message2)  # Самый новый первый
        

class ChatValidatorTest(TestCase):
    
    def test_validate_title_valid(self):
        """Тест валидации заголовка с валидными данными"""

        
        # Проверяем нормальный случай
        result = validate_title("Правильный заголовок")
        self.assertEqual(result, "Правильный заголовок")
        
        # Проверяем обрезку пробелов
        result = validate_title("  Заголовок с пробелами  ")
        self.assertEqual(result, "Заголовок с пробелами")
        
    def test_validate_title_invalid(self):
        """Тест валидации заголовка с невалидными данными"""
        
        # Пустая строка
        with self.assertRaisesMessage(ValidationError, "Заголовок не может быть пустым"):
            validate_title("")
            
        # Только пробелы
        with self.assertRaisesMessage(ValidationError, "Заголовок не может состоять только из пробелов"):
            validate_title("   ")
            
        # Слишком длинный заголовок
        with self.assertRaisesMessage(ValidationError, "Заголовок не может быть длиннее 200 символов"):
            validate_title("x" * 201)


class MessageValidatorTest(TestCase):
    
    def test_validate_text_valid(self):
        """Тест валидации текста сообщения с валидными данными"""
        from chat.validators import validate_text
        
        # Проверяем нормальный случай
        result = validate_text("Правильное сообщение")
        self.assertEqual(result, "Правильное сообщение")
        
    def test_validate_text_invalid(self):
        """Тест валидации текста сообщения с невалидными данными"""
        
        # Пустое сообщение
        with self.assertRaisesMessage(ValidationError, "Текст сообщения не может быть пустым"):
            validate_text("")
            
        # Слишком длинное сообщение
        with self.assertRaisesMessage(ValidationError, "Текст сообщения не может быть длиннее 5000 символов"):
            validate_text("x" * 5001)

        # Текст только с пробелами
        with self.assertRaisesMessage(ValidationError, "Текст сообщения не может состоять только из пробелов"):
            validate_text("   ")



class ValidateLimitTest(TestCase):
    
    def test_validate_limit_valid_range(self):
        """Тест валидации лимита в допустимом диапазоне"""
        
        # Нормальные значения
        self.assertEqual(validate_limit(1), 1)
        self.assertEqual(validate_limit(50), 50)
        self.assertEqual(validate_limit(100), 100)
        
    def test_validate_limit_out_of_range(self):
        """Тест валидации лимита за пределами допустимого диапазона"""
        
        # Значения меньше 1 (должно вернуться значение по умолчанию 20)
        self.assertEqual(validate_limit(0), 20)
        self.assertEqual(validate_limit(-5), 20)
        
        # Значения больше 100 (должно вернуться 100)
        self.assertEqual(validate_limit(101), 100)
        self.assertEqual(validate_limit(1000), 100)


class ChatViewTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.chat_data = {'title': 'Тестовый чат'}
        self.chat = Chat.objects.create(title='Существующий чат')
        
    def test_create_chat(self):
        """Тест создания чата через API"""
        url = reverse('chat-create')
        response = self.client.post(url, self.chat_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 2)
        self.assertEqual(Chat.objects.first().title, 'Тестовый чат')
        
    def test_get_chat_detail(self):
        """Тест получения детальной информации о чате"""
        url = reverse('chat-detail', kwargs={'pk': self.chat.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Существующий чат')
        self.assertIn('messages', response.data)
        
    def test_delete_chat(self):
        """Тест удаления чата"""
        url = reverse('chat-detail', kwargs={'pk': self.chat.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Chat.objects.count(), 0)
        

class MessageViewTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.chat = Chat.objects.create(title='Тестовый чат')
        self.message_data = {'text': 'Тестовое сообщение'}
        
    def test_create_message(self):
        """Тест создания сообщения в чате"""
        url = reverse('message-create', kwargs={'pk': self.chat.pk})
        response = self.client.post(url, self.message_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.last().text, 'Тестовое сообщение')
        self.assertEqual(Message.objects.last().chat_id, self.chat)
        
    def test_create_message_to_nonexistent_chat(self):
        """Тест создания сообщения в несуществующем чате"""
        url = reverse('message-create', kwargs={'pk': 999})
        before = Message.objects.count()

        resp = self.client.post(url, self.message_data, format='json')

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert Message.objects.count() == before
