import hashlib
from Crypto.Cipher import AES
import exceptions


class CryptoAES:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_OCB)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return ciphertext, tag, cipher.nonce

    def decrypt(self, ciphertext, tag, nonce):
        cipher = AES.new(self.key, AES.MODE_OCB, nonce=nonce)
        try:
            result = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            raise exceptions.MessageCorrupt("This message is corrupt.")
        return result
