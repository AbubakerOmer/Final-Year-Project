import os

from django import template
from cryptography.fernet import Fernet
register = template.Library()

def load_key():
    """
    Load the previously generated key
    """
    return open(os.getcwd()+"/chat/"+"secret.key", "rb").read()

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

@register.simple_tag()
def decryptMsg(msg):
    plain_msg=decrypt_message(msg)
    return plain_msg
