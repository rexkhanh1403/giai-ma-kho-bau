# crypto_utils.py

import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

# --- Caesar Cipher ---
def caesar_cipher(text, shift, encode=True):
    """
    Encrypts or decrypts text using Caesar cipher.
    Args:
        text (str): The input text.
        shift (int): The shift value.
        encode (bool): True for encryption, False for decryption.
    Returns:
        str: The processed text.
    """
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            if encode:
                processed_char = chr(start + (ord(char) - start + shift) % 26)
            else:
                processed_char = chr(start + (ord(char) - start - shift + 26) % 26) # +26 for correct modulo with negative results
            result += processed_char
        else:
            result += char
    return result

# --- Vigenere Cipher ---
def vigenere_cipher(text, key, encode=True):
    """
    Encrypts or decrypts text using Vigenere cipher.
    Args:
        text (str): The input text.
        key (str): The Vigenere key.
        encode (bool): True for encryption, False for decryption.
    Returns:
        str: The processed text.
    """
    result = ""
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            key_shift = ord(key[key_index % len(key)]) - ord('A')
            
            if encode:
                processed_char = chr(start + (ord(char.upper()) - ord('A') + key_shift) % 26)
            else:
                processed_char = chr(start + (ord(char.upper()) - ord('A') - key_shift + 26) % 26) # +26 for correct modulo with negative results
            
            result += processed_char if char.isupper() else processed_char.lower()
            key_index += 1
        else:
            result += char
    return result

# --- RSA Encryption/Decryption ---
def generate_rsa_key_pair(key_size=2048):
    """Generates a new RSA private and public key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt(public_key, plaintext):
    """
    Encrypts plaintext using RSA public key.
    Returns base64 encoded ciphertext.
    Note: RSA is for small amounts of data. Larger data needs hybrid encryption (AES+RSA).
    """
    plaintext_bytes = plaintext.encode('utf-8')
    max_chunk_size = public_key.key_size // 8 - 66
    
    if len(plaintext_bytes) > max_chunk_size:
        print(f"Warning: Plaintext is too large for direct RSA encryption. Max size: {max_chunk_size} bytes.")
        return None

    try:
        ciphertext = public_key.encrypt(
            plaintext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode('utf-8')
    except Exception as e:
        print(f"RSA Encryption Error: {e}")
        return None

def rsa_decrypt(ciphertext_b64, private_key):
    """
    Decrypts base64 encoded ciphertext using RSA private key.
    Returns decrypted plaintext string.
    """
    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)

        plaintext = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"RSA Decryption Error: {e}")
        return None

# --- AES Encryption/Decryption ---
def generate_aes_key_and_iv(key_size_bytes=32): # 32 bytes for AES-256
    """Generates a random AES key and IV."""
    key = os.urandom(key_size_bytes)
    iv = os.urandom(16) # IV for AES-CBC or AES-GCM is 16 bytes (128 bits)
    return key, iv

def aes_encrypt(plaintext, key, iv):
    """
    Encrypts plaintext using AES-CBC.
    Returns base64 encoded ciphertext.
    """
    try:
        pad_len = 16 - (len(plaintext.encode('utf-8')) % 16)
        padded_plaintext = plaintext.encode('utf-8') + bytes([pad_len]) * pad_len

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        
        return base64.b64encode(iv + ciphertext).decode('utf-8')
    except Exception as e:
        print(f"AES Encryption Error: {e}")
        return None

def aes_decrypt(ciphertext_b64, key):
    """
    Decrypts base64 encoded ciphertext using AES-CBC.
    Returns decrypted plaintext string.
    The IV is expected to be part of the ciphertext_b64 (first 16 bytes).
    """
    try:
        full_ciphertext_bytes = base64.b64decode(ciphertext_b64)
        
        iv = full_ciphertext_bytes[:16]
        ciphertext = full_ciphertext_bytes[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        pad_len = padded_plaintext[-1]
        plaintext = padded_plaintext[:-pad_len]

        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"AES Decryption Error: {e}")
        return None

