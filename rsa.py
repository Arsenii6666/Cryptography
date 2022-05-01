import re
import random

def Generate_prime_numbers():
    return 83, 79

def check_codivisors(fi, x):
    """
    An auxillary function performing a math.gcd() functional.
    """
    output = []
    for i in range(2, fi):
        if x % i == 0 and fi % i == 0:
            output.append(i)
            break
    return output

def get_the_keys():
    p, q=Generate_prime_numbers()
    n=p*q
    n=n
    fi = (p - 1)*(q - 1)
    e = [x for x in range(2, fi) if \
            not check_codivisors(fi, x)]
    e = e[random.randint(0, len(e) - 1)]
    for x in range(1, fi):
        if (((e % fi) * (x % fi)) % fi == 1):
            d = x
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def encoding(block, key):
    """
    Performs the encoding and decoding procedure using 
    special formulae. block argument is a block of an encoded message
    while key argument is an (int, int) tuple generated 
    by the main function.
    """
    return str((int(block) ** key[0]) % key[1])

def alpha_encode_the_message(message, n):
    """
    Turns letter message into a special code using
    en_alphabet.txt.
    """
    en_alphabet = [x.split(" ") for x in\
open("discrete-math-project3/en_alphabet.txt",\
"r").read().split("\n")]
    for i in en_alphabet:
        message = message.replace(i[1], i[0])
    message=separate_message(message, n)
    return message

def alpha_decode_the_message(message, n):
    """
    Turns the decoded and splitted by blocks message
    into an English one. 
    ["0805", "1212", "15"] 
    would turn into 
    "hello".
    """
    en_alphabet = [x.split(" ") for x in\
open("discrete-math-project3/en_alphabet.txt",\
"r").read().split("\n")]
    block_size = len(str(n)) - len(str(n)) % 2
    for j in range(0, len(message)):
        zeros_to_add = "0" * (block_size - len(message[j]))
        message[j] = zeros_to_add + message[j]
    message = "".join(message)
    message =[x for x in re.findall('..', message) if x != "00"]
    for i in en_alphabet:
        for letter in range(len(message)):
            if i[0] == message[letter]:
                message[letter] = i[1]
    message = "".join(message)
    return message

def separate_message(message, n):
        """
        Separates the encoded message to start its encryption. 
        Turns string code of a message into a list of substrings 
        which have a size of 2n. 
        The examples of an output (not encoded message - "hi"):
        ["08", "09"]
        ["0809"]
        """
        blocks = []
        block_size = len(str(n)) - len(str(n)) % 2
        for i in range(0, len(message), block_size):
            to_append = message[i: i + block_size]
            while len(to_append) != block_size:
                to_append = "0" + to_append
            blocks.append(to_append)
        return blocks

print(get_the_keys())