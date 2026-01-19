from django.core.exceptions import ValidationError


def validate_title(value: str) -> str:
    """Валидатор заголовка.
    
    Проверяет, что заголовок не пустой, не состоит только из пробелов и не превышает 200 символов.
    
    Args:
        value (str): Заголовок для валидации.
        
    Returns:
        str: Очищенный от пробелов в начале и конце заголовок.
        
    Raises:
        ValidationError: Если заголовок не прошёл валидацию.
    """

    if not value:
        raise ValidationError(
            "Заголовок не может быть пустым"
        )

    value = value.strip()

    if not value:
        raise ValidationError(
            "Заголовок не может состоять только из пробелов"
        )

    if len(value) > 200:
        raise ValidationError(
            "Заголовок не может быть длиннее 200 символов"
        )
    return value

def validate_text(value: str) -> str:
    """Валидатор текста сообщения.
    
    Проверяет, что текст не пустой и не превышает 5000 символов.
    
    Args:
        value (str): Текст сообщения для валидации.
        
    Returns:
        str: Исходный текст, если он прошёл валидацию.
        
    Raises:
        ValidationError: Если текст пустой или слишком длинный.
    """
    if not value:
        raise ValidationError(
            "Текст сообщения не может быть пустым"
        )

    stripped_value = value.strip()

    if not stripped_value:
        raise ValidationError(
            "Текст сообщения не может состоять только из пробелов"
        )

    if len(value) > 5000:
        raise ValidationError(
            "Текст сообщения не может быть длиннее 5000 символов"
        )
    return value

def validate_limit(limit: int) -> int:
    """Валидатор лимита.
    
    Преобразует значение лимита в целое число и ограничивает его диапазоном от 1 до 100.
    Если значение меньше 1, устанавливается значение по умолчанию — 20.
    
    Args:
        limit (int): Лимит для валидации.
        
    Returns:
        int: Ограниченное значение лимита в диапазоне от 1 до 100.
    """
    limit = int(limit)
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 20
    return limit
