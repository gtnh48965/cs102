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
        x = ord(i)
        if (x > 64 and x < 123):
            if (87 < x < 91) or (x < 123 and x > 119):
                x = x - 26
            y = chr(x + 3)
            plaintext = plaintext.replace(i, y)
            print(plaintext)
return plaintext

    


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
    
    return plaintext
