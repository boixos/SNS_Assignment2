import os
import sys
import socket
import pickle
import numpy as np
port = 5001
key = '1001'.lstrip('0')
l_key = len(key)


CIPHER_MATRIX = np.array([
    [-3, -3, -4],
    [0, 1, 1],
    [4, 3, 4]
])

CIPHER_MATRIX_INV = np.array([
    [1, 0, 1],
    [4, 4, 3],
    [-4, -3, -3]
])

ENCODING_RULE = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13,
                 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26, ' ': 27}
DECODING_RULE = dict([(value, key) for key, value in ENCODING_RULE.items()]) 


def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


def mod2div(divident, divisor):
    l_key = len(divisor)
    tmp = divident[0: l_key]

    while l_key < len(divident):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[l_key]
        else:   
            tmp = xor('0'*l_key, tmp) + divident[l_key]
        l_key += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*l_key, tmp)
    return tmp


def stringToBinary(data):
    return (''.join(format(ord(x), 'b') for x in data))


def generate_crc(data):
    binary_data = stringToBinary(data)

    # Appends n-1 zeroes at end of data
    binary_data = binary_data + '0'*(l_key-1)
    remainder = mod2div(binary_data, key)
    binary_data = binary_data + remainder
    # print(binary_data)
    return binary_data
