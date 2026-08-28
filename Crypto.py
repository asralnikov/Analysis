"""Да, проверить публичный SSH-ключ программно на Python можно. Это полезно для автоматизации или если вы хотите встроить проверку в свой скрипт.

Для работы с ключами лучше всего подходит библиотека cryptography. Поскольку у вас есть Anaconda, она уже должна быть установлена (или установится одной командой).

1. Установка библиотеки
bash
Копировать
conda install cryptography

(Если conda не найдет пакет, используйте pip: pip install cryptography)

2. Код для проверки длины и отпечатка ключа

Этот скрипт прочитает ваш файл id_rsa.pub, декодирует его и выведет технические параметры:

python
Копировать
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

def check_ssh_public_key(file_path):
    try:
        with open(file_path, 'r') as f:
            # Читаем строку из файла (убираем лишние пробелы)
            line = f.read().strip()
        
        # Строка выглядит так: "ssh-rsa AAAAB3NzaC1yc2E... комментарий"
        parts = line.split(' ', 2)
        
        if len(parts) < 2 or parts[0] != 'ssh-rsa':
            print("Файл не является стандартным публичным RSA-ключом.")
            return

        b64_data = parts[1]
        
        # Декодируем Base64 часть в чистые байты
        key_bytes = base64.b64decode(b64_data)
        
        # Пропускаем служебные поля OpenSSH ('ssh-rsa' + длина строки)
        # Ключ начинается после первых двух length-префиксов
        # Упрощенный способ: просто ищем длину модуля N
        
        from cryptography.hazmat.primitives.asymmetric import rsa
        
        # Загружаем объект открытого ключа
        public_key = serialization.load_ssh_public_key(
            line.encode('utf-8'), 
            backend=default_backend()
        )
        
        # Если это именно RSA, получаем числа
        if isinstance(public_key, rsa.RSAPublicNumbers):
            numbers = public_key.public_numbers()
            modulus_bit_length = numbers.n.bit_length()
            
            print(f"Тип ключа: RSA")
            print(f"Длина модуля (в битах): {modulus_bit_length}")
            
            # Вычисляем SHA256 отпечаток (как делает ssh-keygen -lf)
            import hashlib
            sha256_hash = hashlib.sha256(key_bytes).digest()
            
            # Кодируем в base64 для вывода (аналог формата GitHub)
            fingerprint_b64 = base64.b64encode(sha256_hash).decode('utf-8').replace('=', '')
            print(f"SHA256-отпечаток: {fingerprint_b64}")
            
            # Проверка на соответствие ожидаемым значениям
            if modulus_bit_length == 4096:
                print("\nСтатус: Ключ корректен (RSA 4096)")
            else:
                print(f"\nВнимание: Ожидался ключ 4096 бит, получено {modulus_bit_length}")

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении ключа: {e}")

# Запуск для вашего файла
check_ssh_public_key('/Users/ARalnikov/.ssh/id_rsa.pub')
Что покажет этот скрипт:
Длина модуля (в битах): Для здорового ключа должно быть ровно 4096. Если там число вроде 375 или другое странное значение — значит, при генерации через терминал что-то пошло не так (например, процесс прервался).
SHA256-отпечаток: Короткая строка вида AbCdEfGh.... Именно её нужно сравнивать с той, которую предлагает добавить GitHub в настройках профиля, чтобы убедиться, что вы копируете правильный ключ.
Почему нельзя просто посчитать символы?

Как мы выяснили ранее, длина строки (len(open(...).read())) всегда будет около 700 символов из-за кодировки Base64. Эта величина ничего не говорит о криптографической стойкости. Только побитовая длина самого числа внутри ключа имеет значение, и получить её без парсинга бинарных данных невозможно — здесь как раз и помогает библиотека cryptography.

Альтернатива (без сторонних библиотек)

Если устанавливать пакеты совсем не хочется, можно использовать системную утилиту прямо из Python:

python
Копировать
import subprocess

try:
    result = subprocess.run(['ssh-keygen', '-lf', '/Users/ARalnikov/.ssh/id_rsa.pub'], 
                            capture_output=True, text=True, check=True)
    print(result.stdout.strip())
except subprocess.CalledProcessError as e:
    print(f"Ошибка вызова системы: {e.stderr}")

Это вызовет ту самую команду ssh-keygen -lf, которой мы проверяли ключ вручную, но сделает это изнутри скрипта.
"""
import sys 
print("Скрипт запущен", flush=True)

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import hashlib

def check_key_from_string(key_string):
    try:
        # Загружаем ключ прямо из переданной строки
        public_key = serialization.load_ssh_public_key(
            key_string.encode('utf-8'), 
            backend=default_backend()
        )
        
        from cryptography.hazmat.primitives.asymmetric import rsa
        
        if isinstance(public_key, rsa.RSAPublicNumbers):
            numbers = public_key.public_numbers()
            bit_length = numbers.n.bit_length()
            
            print(f"Длина ключа: {bit_length} бит")
            
            # Для вычисления отпечатка нам нужны чистые байты Base64
            parts = key_string.strip().split(' ', 2)
            b64_data = parts[1]
            key_bytes = base64.b64decode(b64_data)
            
            sha256_hash = hashlib.sha256(key_bytes).digest()
            fingerprint_b64 = base64.b64encode(sha256_hash).decode('utf-8').replace('=', '')
            
            print(f"SHA256-отпечаток: SHA256:{fingerprint_b64}")
            
            if bit_length == 4096:
                print("Ключ корректен.")
            else:
                print("Длина нестандартная!")
                
    except ValueError as e:
        print(f"Ключ поврежден или имеет неверный формат: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# --- КАК ПОЛЬЗОВАТЬСЯ ---

# Вставьте сюда вашу строку целиком (вместо ... ваш_ключ ...)
key_str = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvwzg2kzH3ENMJ6Ly0zIy7qgteTuLopZMOYX43sljC7dtm783zwghhkiRPdOyS4vuFYSV+uiVqQR68th4hTwGPYfOZX8S/ZmTxBUOup4v0GDiks+NB8eavADUDxJr13wBCGGxlKI3hqd5AdQcyMoFBSRYRtxsnIZr025eZD+FLU4iosR6dBPkVjxDTFBWWakCH3Lsk/3cH7aabV1L2eDUf3AV/yi3fw7RzPi3wU2G3ip0uNcLAgYdUe5kSYI89bZH+/rBIPP/0AhMGY5DMtEZPmJmb0DLgi/3KaoYWfYjHjdMG4LLo25ZHltQxh50Sopj7nGx+ZLvvaIUN7+v+3ffBQBOKfswCxt3TYxh/VWid8w/iciyUfz5EU1d3JRCbYqwjComgHrIRJ3MMX5C2TXjTQDjK0xEdD2HY82nscBnaajURVBWgEji0shrtvNOLGM9d2CaLjLBuX1FEA7GbnieKq9zgaqhdR2oUj2xQhg2P2Zd2EmXyJFN6Aer+I162pheMhp+4/e8P2piOg0aqCp5gEjVWUs/0lGiyr+QCod54rn6gWO3qH69PeVn6cf1NxW0xmupewAc7mDIgj6Elnq6GAXYb1BNz+u0gq7oJWhZBQSw9LWUqqFfo4H9TmDgD/IU7+rAF4jSXxfZLheh8P7wY36+CIK4dQ3j++5y3BPv4KQ== aralnikov@gmail.com"

check_key_from_string(key_str)

"""Как это работает внутри Python?

Строка SSH-ключа — это бинарные данные, упакованные в текстовый формат OpenSSH по следующему правилу: <тип> <base64-данные> <комментарий>

Скрипт берет вторую часть (parts[1]) — это закодированные в Base64 внутренние структуры ключа.
С помощью base64.b64decode() он превращает этот текст обратно в «сырые» байты.
Функция serialization.load_ssh_public_key() понимает специфику формата OpenSSH, пропускает служебные заголовки типа ssh-rsa и добирается до самого числа $n$ (модуля RSA).
У этого числа вызывается метод .bit_length(), который математически точно определяет количество значащих бит.

Что делать: замените значение переменной key_str на ту самую длинную строку, которую вы копируете из терминала командой cat ~/.ssh/id_rsa.pub. Запустите код, и он выведет реальную длину в битах и правильный отпечаток."""


from cryptography.hazmat.primitives import serialization

# Вставьте вашу ОДНУ длинную строку сюда между тройными кавычками
key_str = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvwzg2kzH3ENMJ6Ly0zIy7qgteTuLopZMOYX43sljC7dtm783zwghhkiRPdOyS4vuFYSV+uiVqQR68th4hTwGPYfOZX8S/ZmTxBUOup4v0GDiks+NB8eavADUDxJr13wBCGGxlKI3hqd5AdQcyMoFBSRYRtxsnIZr025eZD+FLU4iosR6dBPkVjxDTFBWWakCH3Lsk/3cH7aabV1L2eDUf3AV/yi3fw7RzPi3wU2G3ip0uNcLAgYdUe5kSYI89bZH+/rBIPP/0AhMGY5DMtEZPmJmb0DLgi/3KaoYWfYjHjdMG4LLo25ZHltQxh50Sopj7nGx+ZLvvaIUN7+v+3ffBQBOKfswCxt3TYxh/VWid8w/iciyUfz5EU1d3JRCbYqwjComgHrIRJ3MMX5C2TXjTQDjK0xEdD2HY82nscBnaajURVBWgEji0shrtvNOLGM9d2CaLjLBuX1FEA7GbnieKq9zgaqhdR2oUj2xQhg2P2Zd2EmXyJFN6Aer+I162pheMhp+4/e8P2piOg0aqCp5gEjVWUs/0lGiyr+QCod54rn6gWO3qH69PeVn6cf1NxW0xmupewAc7mDIgj6Elnq6GAXYb1BNz+u0gq7oJWhZBQSw9LWUqqFfo4H9TmDgD/IU7+rAF4jSXxfZLheh8P7wY36+CIK4dQ3j++5y3BPv4KQ== aralnikov@gmail.com"

try:
    public_key = serialization.load_ssh_public_key(key_str.encode('utf-8'))
    
    from cryptography.hazmat.primitives.asymmetric import rsa
    if isinstance(public_key, rsa.RSAPublicNumbers):
        n_bits = public_key.public_numbers().n.bit_length()
        print(f"Длина: {n_bits} бит")
        
        # Проверка типа через строковый разбор (на случай ошибок библиотеки)
        parts = key_str.strip().split()
        b64_data = parts[1]
        raw_bytes = __import__('base64').b64decode(b64_data)
        sha256_hash = __import__('hashlib').sha256(raw_bytes).digest()
        fp = __import__('base64').b64encode(sha256_hash).decode('utf-8').replace('=', '')
        print(f"Отпечаток: SHA256:{fp}")
except:
    print("Ключ поврежден или имеет неверный формат.")


from cryptography.hazmat.primitives import serialization

# Сюда вставьте ТОЛЬКО ту строку, которую пытаетесь отправить на Гитхаб
key_str = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvwzg2kzH3ENMJ6Ly0zIy7qgteTuLopZMOYX43sljC7dtm783zwghhkiRPdOyS4vuFYSV+uiVqQR68th4hTwGPYfOZX8S/ZmTxBUOup4v0GDiks+NB8eavADUDxJr13wBCGGxlKI3hqd5AdQcyMoFBSRYRtxsnIZr025eZD+FLU4iosR6dBPkVjxDTFBWWakCH3Lsk/3cH7aabV1L2eDUf3AV/yi3fw7RzPi3wU2G3ip0uNcLAgYdUe5kSYI89bZH+/rBIPP/0AhMGY5DMtEZPmJmb0DLgi/3KaoYWfYjHjdMG4LLo25ZHltQxh50Sopj7nGx+ZLvvaIUN7+v+3ffBQBOKfswCxt3TYxh/VWid8w/iciyUfz5EU1d3JRCbYqwjComgHrIRJ3MMX5C2TXjTQDjK0xEdD2HY82nscBnaajURVBWgEji0shrtvNOLGM9d2CaLjLBuX1FEA7GbnieKq9zgaqhdR2oUj2xQhg2P2Zd2EmXyJFN6Aer+I162pheMhp+4/e8P2piOg0aqCp5gEjVWUs/0lGiyr+QCod54rn6gWO3qH69PeVn6cf1NxW0xmupewAc7mDIgj6Elnq6GAXYb1BNz+u0gq7oJWhZBQSw9LWUqqFfo4H9TmDgD/IU7+rAF4jSXxfZLheh8P7wY36+CIK4dQ3j++5y3BPv4KQ== aralnikov@gmail.com"

print ('lets go')
try:
    # Попытка загрузить как стандартный OpenSSH
    print ('0')
    pub_key = serialization.load_ssh_public_key(key_str.encode('utf-8'))
    print ('1')
    from cryptography.hazmat.primitives.asymmetric import rsa
    if isinstance(pub_key, rsa.RSAPublicNumbers):
        print("Ключ валиден для Python.")
        
        # Попробуем пересобрать его в идеальный PEM-формат, а потом обратно в OpenSSH
        pem_data = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        clean_ssh_key = serialization.load_pem_public_key(pem_data).public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        ).decode('utf-8')
        
        print("\n--- ИДЕАЛЬНО ЧИСТАЯ СТРОКА ДЛЯ GITHUB ---")
        print(clean_ssh_key)
except :
    print("Ключ не валиден.")