import random
import string
import re

def generate_chat_id() -> str:
    # Gera uma string aleatória de 26 caracteres (letras e números)
    chat_id = ''.join(random.choices(string.ascii_letters + string.digits, k=26))

    # Verifica se o chat_id gerado está no formato correto usando regex
    if re.fullmatch(r'[A-Za-z0-9]{26}', chat_id):
        return chat_id
    else:
        # Caso não esteja no formato correto, gera novamente
        return generate_chat_id()
