import socket
import threading
import message_integrity
import rsa
import random

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
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
        #
        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = (username, c.recv(1024))
            self.clients.append(c)

            # send public key to the client 
            c.send(self.public_key)
            # ...
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        print(msg)
        return
        for client in self.clients: 

            # encrypt the message
            message=rsa.separate_message(rsa.alpha_encode_the_message(message), self.n)
            message=rsa.encoding(message, self.username_lookup[client][1])
            # ...

            client.send(msg.encode())

    def handle_client(self, c: socket, addr): 
        while True:
            msg = c.recv(1024)
            #decrypt msg
            msg=rsa.alpha_decode_the_message(rsa.encoding(msg, self.private_key), self.n)
            #
            for client in self.clients:
                if client != c: #Доробити умову
                    #incrypt msg
                    msg=rsa.encoding(rsa.alpha_encode_the_message(msg, self.n), self.username_lookup[c][1])
                    #
                    client.send(msg)

if __name__ == "__main__":
    s = Server(9001)
    s.start()
