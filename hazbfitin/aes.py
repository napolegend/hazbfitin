"""
Это файл, реализующий логику шифровки-дешифровки сообщений
"""
import hashlib
from Crypto.Cipher import AES
import exceptions


class CryptoAES:
    """
    Это класс шифровщика, каждый клиент создает свой экземпляр данного класса для того,
    чтобы хранить значения ключей и прочее
    """
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, data):
        """
        Эта функция принимает string и возвращает набор значений характерных для
        AES шифрования OCB (новая версия AES предотвращающая подмену сообщений)
        """
        cipher = AES.new(self.key, AES.MODE_OCB)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return ciphertext, tag, cipher.nonce

    def decrypt(self, ciphertext, tag, nonce):
        """
         Эта функция принимает набор значений характерных для AES шифрования OCB и возвращает
         расшифрованный текст в byte формате
        """
        cipher = AES.new(self.key, AES.MODE_OCB, nonce=nonce)
        try:
            result = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            raise exceptions.MessageCorrupt("This message is corrupt.")
        return result
