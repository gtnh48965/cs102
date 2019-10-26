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
    nana = ord('a')
    nanA = ord('A')
    if nana > nanA:
        neyn = nana
    else:
        neyn = nanA
    
    while len(plaintext) > len(keyword):
        keyword += keyword
    ss = len(plaintext) // len(keyword)
    for i, j in enumerate(plaintext):
        if 'a' <= j <= 'z':
            key = (ord(keyword[i % len(keyword)]) - neyn) % 26
            mid = (ord(j) + key - nana) % 26 + nana
            ciphertext += chr(mid)
        elif 'A' <= j <= 'Z':
            key = (ord(keyword[i % len(keyword)]) - neyn) % 26
            mid = (ord(j) + key - nanA) % 26 + nanA
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
    plaintext = " "
    keyword = keyword.lower()
    nana = ord('a')
    nanA = ord('A')
    if nana > nanA:
        neyn = nana
    else:
        neyn = nanA

    while len(ciphertext) > len(keyword):
        keyword += keyword
    ss = len(ciphertext) // len(keyword)
    for i, j in enumerate(ciphertext):
        if 'a' <= j <= 'z':
            key = (ord(keyword[i % len(keyword)]) - neyn) % 26
            mid = (ord(j) - key - nana) % 26 + nana
            plaintext += chr(mid)
        elif 'A' <= j <= 'Z':
            key = (ord(keyword[i % len(keyword)]) - neyn) % 26
            mid = (ord(j) - key - nanA) % 26 + nanA
            plaintext += chr(mid)
        else:
            plaintext += j

    return plaintext
