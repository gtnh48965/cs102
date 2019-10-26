def encrypt_caesar(plaintext: str) -> str:
    """
        Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    for i in plaintext:

        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            if ('a' <= i <= 'w') or ('A' <= i <= 'W'):
                y = chr(ord(i) + 3)
            else:
                y = chr(ord(i) - 23)
        else:
            i += y
        plaintext = plaintext.replace(i, y)

    return plaintext

def decrypt_caesar(ciphertext: str) -> str:
    """
     >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
     >>> decrypt_caesar("sbwkrq")
     'python'
     >>> decrypt_caesar("Sbwkrq3.6")
     'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    for i in ciphertext:

        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            if ('c' <= i <= 'z') or ('C' <= i <= 'Z'):
                y = chr(ord(i) - 3)
            else:
                y = chr(ord(i) + 23)
        else:
            i += y
        ciphertext = ciphertext.replace(i, y)
    return ciphertext