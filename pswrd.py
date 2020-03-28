import hashlib
from Crypto.Cipher import AES

def pad(text):
    while len(text) % 32 != 0:
        text += b' '
    return text

right_pass = bytes(input('Input right pass '), encoding='utf-8')
print(right_pass)
text = pad(b'my some secure text')

right_key = hashlib.sha256(right_pass).digest()

right_aes = AES.new(right_key, AES.MODE_ECB)
ciphered = right_aes.encrypt(text)
print(f"{text=} {ciphered=}")

while True:

    password = bytes(input('Input your pass '), encoding='utf8')
    print(password)
    
    key = hashlib.sha256(password).digest()

    try_aes = AES.new(key, AES.MODE_ECB)
    try_text = try_aes.decrypt(ciphered)
    print(try_text)
