# import os 
# print("OS OK")
# print ('go')
# from cryptography.hazmat.primitives import serialization
# print ('lets go')
# # Сюда вставьте ТОЛЬКО ту строку, которую пытаетесь отправить на Гитхаб
# key_str = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvwzg2kzH3ENMJ6Ly0zIy7qgteTuLopZMOYX43sljC7dtm783zwghhkiRPdOyS4vuFYSV+uiVqQR68th4hTwGPYfOZX8S/ZmTxBUOup4v0GDiks+NB8eavADUDxJr13wBCGGxlKI3hqd5AdQcyMoFBSRYRtxsnIZr025eZD+FLU4iosR6dBPkVjxDTFBWWakCH3Lsk/3cH7aabV1L2eDUf3AV/yi3fw7RzPi3wU2G3ip0uNcLAgYdUe5kSYI89bZH+/rBIPP/0AhMGY5DMtEZPmJmb0DLgi/3KaoYWfYjHjdMG4LLo25ZHltQxh50Sopj7nGx+ZLvvaIUN7+v+3ffBQBOKfswCxt3TYxh/VWid8w/iciyUfz5EU1d3JRCbYqwjComgHrIRJ3MMX5C2TXjTQDjK0xEdD2HY82nscBnaajURVBWgEji0shrtvNOLGM9d2CaLjLBuX1FEA7GbnieKq9zgaqhdR2oUj2xQhg2P2Zd2EmXyJFN6Aer+I162pheMhp+4/e8P2piOg0aqCp5gEjVWUs/0lGiyr+QCod54rn6gWO3qH69PeVn6cf1NxW0xmupewAc7mDIgj6Elnq6GAXYb1BNz+u0gq7oJWhZBQSw9LWUqqFfo4H9TmDgD/IU7+rAF4jSXxfZLheh8P7wY36+CIK4dQ3j++5y3BPv4KQ== aralnikov@gmail.com"


# try:
#     # Попытка загрузить как стандартный OpenSSH
#     print ('0')
#     pub_key = serialization.load_ssh_public_key(key_str.encode('utf-8'))
#     print ('1')
#     from cryptography.hazmat.primitives.asymmetric import rsa
#     print ('2')
#     if isinstance(pub_key, rsa.RSAPublicNumbers):
#         print("Ключ валиден для Python.")
        
#         # Попробуем пересобрать его в идеальный PEM-формат, а потом обратно в OpenSSH
#         pem_data = pub_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo
#         )
#         print ('3')
#         clean_ssh_key = serialization.load_pem_public_key(pem_data).public_bytes(
#             encoding=serialization.Encoding.OpenSSH,
#             format=serialization.PublicFormat.OpenSSH
#         ).decode('utf-8')
        
#         print("\n--- ИДЕАЛЬНО ЧИСТАЯ СТРОКА ДЛЯ GITHUB ---")
#         print(clean_ssh_key)
# except :
#     print("Ключ не валиден.")

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

key_str = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvwzg2kzH3ENMJ6Ly0zIy7qgteTuLopZMOYX43sljC7dtm783zwghhkiRPdOyS4vuFYSV+uiVqQR68th4hTwGPYfOZX8S/ZmTxBUOup4v0GDiks+NB8eavADUDxJr13wBCGGxlKI3hqd5AdQcyMoFBSRYRtxsnIZr025eZD+FLU4iosR6dBPkVjxDTFBWWakCH3Lsk/3cH7aabV1L2eDUf3AV/yi3fw7RzPi3wU2G3ip0uNcLAgYdUe5kSYI89bZH+/rBIPP/0AhMGY5DMtEZPmJmb0DLgi/3KaoYWfYjHjdMG4LLo25ZHltQxh50Sopj7nGx+ZLvvaIUN7+v+3ffBQBOKfswCxt3TYxh/VWid8w/iciyUfz5EU1d3JRCbYqwjComgHrIRJ3MMX5C2TXjTQDjK0xEdD2HY82nscBnaajURVBWgEji0shrtvNOLGM9d2CaLjLBuX1FEA7GbnieKq9zgaqhdR2oUj2xQhg2P2Zd2EmXyJFN6Aer+I162pheMhp+4/e8P2piOg0aqCp5gEjVWUs/0lGiyr+QCod54rn6gWO3qH69PeVn6cf1NxW0xmupewAc7mDIgj6Elnq6GAXYb1BNz+u0gq7oJWhZBQSw9LWUqqFfo4H9TmDgD/IU7+rAF4jSXxfZLheh8P7wY36+CIK4dQ3j++5y3BPv4KQ== aralnikov@gmail.com"""

# try:
#     # Загружаем ключ (мы уже знаем, что сюда он заходит)
#     pub_key = serialization.load_ssh_public_key(key_str.encode('utf-8'))
    
#     print("Ключ успешно загружен библиотекой.")
    
#     # Проверяем тип напрямую
#     if isinstance(pub_key, rsa.RSAPublicNumbers):
#         print("Тип подтвержден: RSA")
        
#         # --- ГЛАВНОЕ ИЗМЕНЕНИЕ ЗДЕСЬ ---
#         # Вместо сложной пересборки через PEM, просто выведем оригинал,
#         # предварительно убедившись, что там нет случайных символов переноса строки.
        
#         clean_key = " ".join(key_str.split())
        
#         print("\n--- СТРОКА ДЛЯ GITHUB ---")
#         print(clean_key)
        
# except Exception as e:
#     # Теперь будем видеть конкретную ошибку
#     print(f"Критическая ошибка: {e}")

# ... ваш импорт ...

raw_key = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvwzg2kzH3ENMJ6Ly0zIy7qgteTuLopZMOYX43sljC7dtm783zwghhkiRPdOyS4vuFYSV+uiVqQR68th4hTwGPYfOZX8S/ZmTxBUOup4v0GDiks+NB8eavADUDxJr13wBCGGxlKI3hqd5AdQcyMoFBSRYRtxsnIZr025eZD+FLU4iosR6dBPkVjxDTFBWWakCH3Lsk/3cH7aabV1L2eDUf3AV/yi3fw7RzPi3wU2G3ip0uNcLAgYdUe5kSYI89bZH+/rBIPP/0AhMGY5DMtEZPmJmb0DLgi/3KaoYWfYjHjdMG4LLo25ZHltQxh50Sopj7nGx+ZLvvaIUN7+v+3ffBQBOKfswCxt3TYxh/VWid8w/iciyUfz5EU1d3JRCbYqwjComgHrIRJ3MMX5C2TXjTQDjK0xEdD2HY82nscBnaajURVBWgEji0shrtvNOLGM9d2CaLjLBuX1FEA7GbnieKq9zgaqhdR2oUj2xQhg2P2Zd2EmXyJFN6Aer+I162pheMhp+4/e8P2piOg0aqCp5gEjVWUs/0lGiyr+QCod54rn6gWO3qH69PeVn6cf1NxW0xmupewAc7mDIgj6Elnq6GAXYb1BNz+u0gq7oJWhZBQSw9LWUqqFfo4H9TmDgD/IU7+rAF4jSXxfZLheh8P7wY36+CIK4dQ3j++5y3BPv4KQ== aralnikov@gmail.com"""

try:
    # Разбиваем строку по пробелам и собираем заново без лишних символов
    parts = raw_key.split()
    
    # Проверяем комментарий (последняя часть)
    comment = parts[-1]
    
    # Собираем чистый ключ: тип + зашифрованная часть
    clean_ssh_string = f"{parts[0]} {parts[1]}"
    
    print("Загружаем очищенный ключ...")
    pub_key = serialization.load_ssh_public_key(clean_ssh_string.encode('utf-8'))
    print("Загрузили...")
    if isinstance(pub_key, rsa.RSAPublicNumbers):
        numbers = pub_key.public_numbers()
        print(f"Ключ валиден. Длина модуля: {numbers.n.bit_length()} бит.")
        
        # Теперь пересобираем ПОЛНУЮ строку для GitHub с чистым комментарием
        final_output = f"{clean_ssh_string} {comment}"
        
        print("\n--- ИДЕАЛЬНО ЧИСТАЯ СТРОКА ---")
        print(final_output)
except :
    print("Ошибка при разборе строки")