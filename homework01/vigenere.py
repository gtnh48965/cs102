def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
        Encrypts plaintext using a Vigenere cipher.
        
        >>> encrypt_vigenere("PYTHON", "A")
        'PYTHON'
        >>> encrypt_vigenere("python", "a")
        'python'
        >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
        'LXFOPVEFRNHR'
        """
    # PUT YOUR CODE HE
    ciphertext = " "
    keyword =keyword.lower()
    
    while len(plaintext) > len(keyword):
        keyword += keyword
    ss = len(plaintext) // len(keyword)
    for i, j in enumerate(plaintext):
        if 'a' <= j <= 'z':
            key=(ord(keyword[i % len(keyword)]) - 97)%26
            mid = (ord(j) + key -97)%26 +97
            ciphertext += chr (mid)
        elif 'A' <= j <= 'Z':
            key = (ord(keyword[i % len(keyword)]) - 97) % 26
            mid = (ord(j) + key - 65) % 26 + 65
            ciphertext += chr(mid)
        else:
            ciphertext += j


return ciphertext



def decrypt_vigenere(ciphertext, keyword):
    """
        Decrypts a ciphertext using a Vigenere cipher.
        
        >>> decrypt_vigenere("PYTHON", "A")
        'PYTHON'
        >>> decrypt_vigenere("python", "a")
        'python'
        >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
        'ATTACKATDAWN'
        """
    # PUT YOUR CODE HERE


return plaintext
