import socket
import threading
import random
import rsa
import message_integrity

class Client:

    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())
        #
        p, q=rsa.Generate_prime_numbers()
        n=p*q
        self.n=n
        fi = (p - 1)*(q - 1)
        e = [x for x in range(2, fi) if \
             not rsa.check_codivisors(fi, x)]
        e = e[random.randint(0, len(e) - 1)]
        d = pow(e, -1, fi)
        self.public_key = (e, n)
        self.private_key = (d, n)
        self.s.send(self.public_key) #!!!
        #
        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message = self.s.recv(1024).decode()
            #
            message=rsa.alpha_decode_the_message(rsa.encoding(message, self.private_key), self.n)
            #
            print(message)

    def write_handler(self):
        while True:
            message = input()
            #
            message=rsa.separate_message(rsa.alpha_encode_the_message(message), self.n)
            message=rsa.encoding(message, self.public_key)
            #
            self.s.send(message)

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
