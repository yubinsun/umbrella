import socket
import time

HOST = ''    # The remote host
PORT = 50007              # The same port as used by the server

counter = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        t = '<cpkg>'
        for i in range(400*400):
            t += chr(counter)
        t += '</cpkg>'
        t = t.encode()
        s.sendall(t)
        print(len(t))
        counter = (counter+10)%100
        print(counter)
        time.sleep(0.05)
        
