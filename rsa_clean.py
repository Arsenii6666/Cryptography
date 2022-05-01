"""
A version of program using classes, not bare functions.
"""

import random
import re

class Encryptor():
    """
    Creates an objects saving all the info refering to the encryption.
    message : str - the message written by user using input.
    p, q : int - any prime numbers
    """
    def __init__(self, message, p, q) -> None:
        self.message = message
        self.p = p
        self.q = q
        self.n = p * q
        self.en_alphabet = [x.split(" ") for x in\
open("discrete-math-project3/en_alphabet.txt",\
"r").read().split("\n")]
        self.en_alphabet.append([str(int(self.en_alphabet[-1][0])+1), " "])
        self.alpha_encode_the_message()

    def alpha_encode_the_message(self):
        """
        Turns letter message into a special code using
        en_alphabet.txt.
        """
        for i in self.en_alphabet:
            self.message = self.message.replace(i[1], i[0])

    def alpha_decode_the_message(self):
        """
        Turns the decoded and splitted by blocks message
        into an English one. 
        ["0805", "1212", "15"] 
        would turn into 
        "hello".
        """
        for j in range(0, len(self.message)):
            zeros_to_add = "0" * (self.block_size - len(self.message[j]))
            self.message[j] = zeros_to_add + self.message[j]
        self.message = "".join(self.message)
        self.message =[x for x in re.findall('..', self.message) if x != "00"]
        for i in self.en_alphabet:
            for letter in range(len(self.message)):
                if i[0] == self.message[letter]:
                    self.message[letter] = i[1]
        self.message = "".join(self.message)

    def encrypt_message(self):
        """
        The main function of an object. Cast it to have an access to
        .blocks and .message properties (encoded and decoded message respectively)
        of this object. 
        """
        self.fi = (self.p - 1) * (self.q - 1)
        self.e = [x for x in range(2, self.fi) if \
             not self.check_codivisors(x)]
        self.e = self.e[random.randint(0, len(self.e) - 1)]
        self.d = pow(self.e, -1, self.fi)
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)
        self.separate_message()
        for i in range(len(self.blocks)):
            self.blocks[i] = self.encoding(self.blocks[i], self.public_key)
        self.decrypt_blocks()

    def encoding(self, block, key):
        """
        Performs the encoding and decoding procedure using 
        special formulae. block argument is a block of an encoded message
        while key argument is an (int, int) tuple generated 
        by the main function.
        """
        return str((int(block) ** key[0]) % key[1])

    def separate_message(self):
        """
        Separates the encoded message to start its encryption. 
        Turns string code of a message into a list of substrings 
        which have a size of 2n. 
        The examples of an output (not encoded message - "hi"):
        ["08", "09"]
        ["0809"]
        """
        self.blocks = []
        self.block_size = len(str(self.n)) - len(str(self.n)) % 2
        for i in range(0, len(self.message), self.block_size):
            to_append = self.message[i: i + self.block_size]
            while len(to_append) != self.block_size:
                to_append = "0" + to_append
            self.blocks.append(to_append)

    def check_codivisors(self, x):
        """
        An auxillary function performing a math.gcd() functional.
        """
        output = []
        for i in range(2, self.fi):
            if x % i == 0 and self.fi % i == 0:
                output.append(i)
                break
        return output

    def decrypt_blocks(self):
        """
        Checks if a decryption of a message is proper.
        Creates a .message property to get the initial message
        which user inputs at the beggining.
        """
        self.message = []
        for i in self.blocks:
            self.message.append(str(self.encoding(i, self.private_key)))
        self.alpha_decode_the_message()


def encryption_launcher(message_to_encode):
    """
    The main of this program. Prints message encoded and
    decoded stance.
    """
    current_encryptor = Encryptor(message_to_encode, 83, 79)
    current_encryptor.encrypt_message()
    print(current_encryptor.blocks)
    print(current_encryptor.message)
    del current_encryptor

if __name__ == "__main__":
    command = input("Type any letter to write a message, 0 to exit :\n>>> ")
    while command != "0":
        encryption_launcher(input("Type your message to your friend :\n>>> "))
        command = input("Type any letter to write a message, 0 to exit :\n>>> ")
