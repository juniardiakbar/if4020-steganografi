def encrypt_vigenere(plainText, key):
    output = ""
    key = key.upper()

    for i in range(0, len(plainText)):
        output += chr((ord(plainText[i]) + ord(key[i % len(key)])) % 256)

    return output


def decrypt_vigenere(cipherText, key):
    output = ""
    key = key.upper()

    for i in range(0, len(cipherText)):
        output += chr((ord(cipherText[i]) - ord(key[i % len(key)])) % 256)

    return output
